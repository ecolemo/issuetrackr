import os
import sys
sys.path.append('/home/ubuntu')
sys.path.append('/home/ubuntu/issuetrackr')
os.environ['DJANGO_SETTINGS_MODULE'] = 'issuetrackr.settings_production'
os.environ['HOME'] = '/home/ubuntu'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
