def handle_upload_file(f):
    with open('/tmp/upload.jpg', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
