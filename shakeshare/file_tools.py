from datetime import datetime
from shakeshare.models import File
from shakeshare.models import Session

def handle_upload_file(session_id, f):
    prefix = '/tmp/'
    orig_name = f.name
    filename = session_id + '__' + unicode(datetime.now()) + '__' + orig_name 
    size = f.size
    path = prefix + filename
    session = Session.objects.get(id=session_id)
    file_entry = File(session_id = session, name = orig_name, size = size, path = path, thumb_path ='') 
    file_entry.save()
    
    with open(prefix + filename, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
