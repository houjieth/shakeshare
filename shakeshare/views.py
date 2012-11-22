from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from file_tools import handle_upload_file
from matching_tools import find_matching_shakes_by_time
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime
from datetime import timedelta
from django.views.decorators.cache import never_cache
from string import split

from shakeshare.models import Session
from shakeshare.models import File
from shakeshare.models import Shake

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
    session = Session(create_time = ctime, expire_time = etime)
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
    '''
    # dummy impl
    shake = Shake.objects.get(session_id=10)
    str = "original shake: " + unicode(shake) 
    str += " matching shake(s): "
    matching_shakes = find_matching_shakes_by_time(shake)
    for s in matching_shakes:
        str += unicode(s) + ' '
    '''

    session_id = request.GET.get('sessionid', 'null')
    is_uploader = request.GET.get('is_uploader', 'null')
    t = get_template('shake.html')

    # If we are entering '/shake' from a existing uploading session
    #   since there is already a session, we don't need to create a new one
    # If we are entering '/shake' by clicking the shake button
    #   then weneed to create a new session
    if session_id is 'null': 
        ctime = datetime.now()
        etime = ctime + timedelta(hours=3) 
        session = Session(create_time = ctime, expire_time = etime)
        session.save()
        session_id = session.id

    c = Context({'session_id':session_id}, {'is_uploader':is_uploader})
    return HttpResponse(t.render(c))

