from django.conf.urls import patterns,include,url
urlpatterns = patterns('main.views',
        url(r'^post/$','categorize_links'),
        url(r'^dashboard/$','feed'),
        url(r'^([\w._-]+)/$','profile'),
        url(r'^genre/([\w ]+)/$','genrefeed'),
        url(r'^show_similar/(\w+)/$','show_similar'),
        url(r'^read_more/(\w+)/$','read_more'),
        )
