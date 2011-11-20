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
    read_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()
    tags = models.ManyToManyField(Tag)

    def update_tags(self, tag_str):
        self.tags.clear()
        tags = tag_str.split(',')
        for tag in tags:
            if tag.strip() == '': continue
            self.tags.add(Tag.objects.get_or_create(name=tag.strip())[0])

    @property
    def vote_score(self):
        return self.vote_set.filter(is_agree=1).count() - self.vote_set.filter(is_agree=0).count()

    def __unicode__(self):
        return self.title

    def save_history(self):
        history = self.issuehistory_set.create(writer=self.writer, title=self.title, content=self.content, status=self.status, created=self.updated)
        history.tags = self.tags.all()
        history.save()

class Comment(models.Model):
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    content = models.TextField()
    status = models.CharField(max_length=50, default='open')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'from %s :[%d][%s]' % (self.issue.title,self.id,self.writer.username)

class IssueHistory(models.Model):
    target = models.ForeignKey(Issue)
    writer = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=50, default='open')
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return str(self.created)

    def restore(self):
        issue = self.target
        issue.title = self.title
        issue.content = self.content
        issue.writer = self.writer
        issue.status = self.status
        issue.tags = self.tags.all()
        issue.save()
        issue.save_history()

class CommentHistory(models.Model):
    target = models.ForeignKey(Comment)
    writer = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    content = models.TextField()
    status = models.CharField(max_length=50, default='open')
    created = models.DateTimeField(auto_now_add=True)


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

class Vote(models.Model):
    voter = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    is_agree = models.BooleanField(default=1)
    created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.voter.username + ":" + str(self.is_agree)