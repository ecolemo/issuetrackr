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
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    filename = models.CharField(max_length=200)
    
    def url(self):
        return '/attachments/%d' % self.id