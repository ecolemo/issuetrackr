from django.contrib import admin
from issue.models import Issue, Comment, Attachment, Tag

admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Tag)