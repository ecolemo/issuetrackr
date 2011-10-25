from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    writer = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=50, default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    content = models.TextField()
    status = models.CharField(max_length=50, default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class Attachment(models.Model):
    storage_path = '~/issuetrackr_files'
    
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    filename = models.CharField(max_length=200)
    size = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def url(self):
        return '/attachments/%d' % self.id
    
    @property
    def file_object(self):
        return file(self.storage_path + '/' + self.id, 'rw')