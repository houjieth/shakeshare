import os
import sys

path = '/projects/shakeshare'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'shakeshare.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
