from django.db import models
from django.contrib.auth.models import User
import os

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
class Issue(models.Model):
    writer = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=50, default='open')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def update_tags(self, tag_str):
        self.tags.all().delete()
        tags = tag_str.split(',')
        for tag in tags:
            if tag.strip() == '': continue
            self.tags.add(Tag.objects.get_or_create(name=tag.strip())[0])
    
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    content = models.TextField()
    status = models.CharField(max_length=50, default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class Attachment(models.Model):
    storage_path = os.environ['HOME'] + '/issuetrackr_files'
    
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue, null=True)
    filename = models.CharField(max_length=200)
    size = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def url(self):
        return '/attachments/%d' % self.id
    
    @property
    def file_object(self):
        return file(self.storage_path + '/%d' % self.id, 'rw')
    
    def save_file(self, f):
        destination = open('%s/%d' % (self.storage_path, self.id), 'wb')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

    def __unicode__(self):
        return self.filename
