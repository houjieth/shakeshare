from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from file_tools import handle_upload_file
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def hello(request):
    return HttpResponse("Hello world")

def landing(request):
    t = get_template('landing.html')
    html = t.render(Context())
    return HttpResponse(html)

def share(request):
    t = get_template('share.html')
    html = t.render(Context())
    return HttpResponse(html)

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        handle_upload_file(request.FILES['file'])
        return HttpResponse("upload succeed")
    return HttpResponse("upload succeed")
