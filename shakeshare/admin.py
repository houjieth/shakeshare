from django.contrib import admin
from shakeshare.models import Session
from shakeshare.models import File
from shakeshare.models import Shake
from shakeshare.models import Match

admin.site.register(Session)
admin.site.register(File)
admin.site.register(Shake)
admin.site.register(Match)

