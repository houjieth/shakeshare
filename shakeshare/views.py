from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from file_tools import handle_upload_file
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime
from datetime import timedelta

from shakeshare.models import Session
from shakeshare.models import File

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
def upload(request):
    if request.method == 'POST':
        session_id = request.POST['current-session-id']
        handle_upload_file(session_id, request.FILES['file'])
        #return HttpResponse("upload succeed")
        return HttpResponse(session_id)
    return HttpResponse("upload failed")
