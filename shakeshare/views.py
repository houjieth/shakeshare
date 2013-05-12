from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from file_tools import handle_upload_file
from matching_tools import find_matching_shakes
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime
from datetime import timedelta
from django.views.decorators.cache import never_cache
from string import split
from time import sleep

from shakeshare.models import Session
from shakeshare.models import File
from shakeshare.models import Shake
from shakeshare.models import Match

import json
import logging

logger = logging.getLogger(__name__)

def hello(request):
    return HttpResponse("Hello world")

def landing(request):
    t = get_template('landing.html')
    html = t.render(Context())
    return HttpResponse(html)

def share(request):
    # for each share request, create a session
    ctime = datetime.now()
    etime = ctime + timedelta(hours=3) 

    # only the uploader can reach here
    session = Session(create_time = ctime, expire_time = etime, is_uploader = True, user_name = 'uploader', associated_sessions = 'null')
    session.save()
    t = get_template('share.html')
    c = Context({"session_id":session.id})
    html = t.render(c)
    return HttpResponse(html)

@csrf_exempt
@never_cache
def upload(request):
    timestamp = request.path.split('/')[-1]
    if request.method == 'POST':
        session_id = request.POST['current-session-id']
        handle_upload_file(session_id, request.FILES['file'])
        return HttpResponse(timestamp)
    #return HttpResponse("upload failed")
    return HttpResponse(timestamp)

def shake(request):
    session_id = request.GET.get('sessionid', 'null')
    is_uploader = False # just a default value
    t = get_template('shake.html')

    # If we are entering '/shake' from a existing uploading session
    #   since there is already a session, we don't need to create a new one
    # If we are entering '/shake' by clicking the shake button
    #   then we need to create a new session

    if session_id is 'null': 
        ctime = datetime.now()
        etime = ctime + timedelta(hours=3) 
        session = Session(create_time = ctime, expire_time = etime, is_uploader = False, user_name = 'null', associated_sessions = 'null')
        session.save()
        session_id = session.id
        is_uploader = False
    else:
        session = Session.objects.get(id=session_id)
        is_uploader = session.is_uploader
        
    logger.debug("session " + unicode(session_id) + " is waiting for shake. is_uploader: " + unicode(is_uploader))

    c = Context({'is_uploader':is_uploader, 'session_id':session_id})
    return HttpResponse(t.render(c))

@csrf_exempt
def match(request):
    session_id = request.POST['session_id']
    is_uploader = request.POST['is_uploader']
    time = request.POST['time']

    latitude = 0
    longitude = 0
    accuracy = 0

    #latitude = float(request.POST['latitude'])
    #longitude = float(request.POST['longitude'])
    #accuracy = float(request.POST['accuracy'])

    logger.debug("session " + session_id + " shaked. is_uploader " + is_uploader + " ,time: " + time + " latitude " + unicode(latitude) + " longtitude " + unicode(longitude) + " accuracy " + unicode(accuracy))

    # Every time we shake, we create a shake object
    shake = Shake()
    shake.session_id = Session.objects.get(id=session_id)
    if is_uploader == 'True':
        shake.is_from_uploader = True
    else:
        shake.is_from_uploader = False
    shake.time = datetime.fromtimestamp(float(time))
    shake.latitude = latitude
    shake.longitude = longitude
    shake.accuracy = accuracy

    shake.save()
    logger.debug("session " + session_id + " a new shake object is made. id: " + unicode(shake.id))
    logger.debug("session " + session_id  + " will try to find match")

    # Due to difference in network conditions, some shake may arrive late
    # So we have to wait for a while before we search for other shakes.
    # However, we want to return to the user with result as soon as possible.
    # So we will split the wait into several parts. As soon as we find the result,
    # we are going to return it immediately

    wait_time_total = 0 # in seconds
    wait_time = 1 # in seconds
    while wait_time_total < 7:
        sleep(wait_time)
        matching_shakes = find_matching_shakes(shake)
        logger.debug("session " + session_id + " with shake " + unicode(shake.id) + " is finding matches."  + " matching_shakes count: " + unicode(len(matching_shakes)))  
        file_id_list = []
        for matching_shake in matching_shakes:
            if matching_shake.is_from_uploader is True:
                uploader_session_id = matching_shake.session_id
                files = list(File.objects.filter(
                            session_id=uploader_session_id))
                logger.debug("session " + session_id + " matches a uploader-session " + session_id + " with shake " + unicode(matching_shake.id) + ", files count: " + unicode(len(files)))
                for f in files:
                    file_id_list.append(f.id)
        if len(file_id_list) > 0: # uploader found, ready to return
            match = Match()
            match.file_id_list = json.dumps(file_id_list)
            match.save()
            return HttpResponse(match.id)
        else: # uploader not found, wait and retry
            wait_time_total += wait_time
            wait_time *= 2
    
    return HttpResponse("match_not_found")

def pool(request):
    match_id = request.GET.get('match_id', 'null')
    match = Match.objects.get(id=match_id)

    json_decoder = json.decoder.JSONDecoder()
    file_id_list = json_decoder.decode(match.file_id_list)

    '''
    fileIds = []
    for file_id in file_id_list:
        f = File.objects.get(id=file_id)
        fileURLs.append(f.path)
    '''

    t = get_template('pool.html')
    c = Context({'fileIds':file_id_list, 'fileCount':len(file_id_list)})

    return HttpResponse(t.render(c))
        

def file(request):
    file_id = request.GET.get('id', 'null')
    f = File.objects.get(id=file_id)
    file_path = f.path
    f_data = open(f.path, 'r')
    response = HttpResponse(f_data, content_type='application/image')
    response['Content-Disposition'] = 'attachment; filename="' + f.name + '"'

    return response

def synctime(request):
    ctime = datetime.now()

    return HttpResponse(ctime.strftime("%s"))

@csrf_exempt
@never_cache
def setname(request):
    session_id = request.POST['session_id']
    user_name = request.POST['name']
    session = Session.objects.get(id=session_id)
    session.user_name = user_name
    session.save()

    return HttpResponse("OK")

def getnames(request):
    cur_time = datetime.now()
    delta = timedelta(seconds=60)
    time_lower_bound = cur_time - delta
    available_sessions = list(Session.objects.filter(
            create_time__range=(time_lower_bound, cur_time)))
    logger.debug(available_sessions)

    # generate json response
    entries = []
    response = {}
    for session in available_sessions:
        entry = {}
        entry['name'] = session.user_name
        entry['session_id'] = session.id
        entries.append(entry);
    response['available_users'] = entries

    return HttpResponse(json.dumps(response), mimetype="application/json")
