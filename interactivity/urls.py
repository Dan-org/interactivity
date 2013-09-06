from django.conf.urls import patterns, include, url
from interactivity import amfgateway

urlpatterns = patterns('',    
    url(r'^hi',                                 'interactivity.views.hi'),    
    url(r'^all/$', 								'interactivity.views.all_interactivities',      name="all_interactivities"),
    url(r'^exercise/(?P<exercise_id>[\w-]+)/$', 'interactivity.views.exercise',                 name="exercise"),
    url(r'',                                    'interactivity.amfgateway.interactivityGateway'),    
)