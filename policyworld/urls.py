from django.conf.urls import patterns, include, url



### Urls
urlpatterns = patterns('',
    #url(r'requirement/(?P<id>\d+)/$', 'badges.views.requirement', name="requirement"),
    #url(r'requirement/(?P<id>\d+)/$', 'badges.views.requirement', name="requirement"),
    #url(r'(?P<id>\d+)/favorite/$', 'badges.views.favorite', name="favorite"),
    #url(r'(?P<id>\d+)/$', 'badges.views.detail', name="detail"),

    url(r'^$', 'policyworld.views.home', name='policyworldgrader'),

    url(r'exercise/(?P<id>\d+)/$', 	'policyworld.views.exercise', 	name='policyworldexercise'),
    url(r'work/(?P<id>\d+)/$', 		'policyworld.views.work', 		name='policyworldwork'),
)
