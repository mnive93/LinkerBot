from django.conf.urls import patterns, include, url
from authentication.views import home
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('authentication.views',
        url(r'^$', 'landing'),
        )
urlpatterns += patterns('',
        url(r'^',include('main.urls')),
        url(r'^accounts/',include('authentication.urls')),
        )
import os
media = os.path.join(os.path.dirname(__file__),'media')
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$','django.views.static.serve',
            {'document_root':media}),
        )

