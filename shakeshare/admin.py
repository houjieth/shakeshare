from django.contrib import admin
from shakeshare.models import Session
from shakeshare.models import File

class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    fields = ['create_time', 'expire_time', 'id']

admin.site.register(Session, SessionAdmin)
admin.site.register(File)

