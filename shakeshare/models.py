from django.db import models

class Session(models.Model):
    create_time = models.DateTimeField()
    expire_time = models.DateTimeField()

    def __unicode__(self):
        return "create_time: " + unicode(self.create_time) + ", expire_time: " + unicode(self.expire_time) + ", session_id: " + unicode(self.id)

class File(models.Model):
    session_id = models.ForeignKey(Session) 
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    path = models.CharField(max_length=100)
    thumb_path = models.CharField(max_length=100)

    def __unicode__(self):
        return "name: " + self.name + ", path: " + self.path + ", session_id: " + unicode(self.session_id.id)

