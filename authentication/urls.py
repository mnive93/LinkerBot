from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from .utils import lr
urlpatterns = patterns('',
	(r'login/$', lr(login)),
    )
urlpatterns += patterns('authentication.views',
    (r'^step2/$','step2'),
    (r'^followtopic/(\w+)','follow_topic'),
    )


