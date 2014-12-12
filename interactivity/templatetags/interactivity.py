#http://cookingupawebsiteindjango.blogspot.com/2009/05/custom-template-tags-part-3-last-minute.html

import os, re, urlparse, uuid
from django import template
from django.template.defaulttags import URLNode, url
from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from xml.etree import ElementTree

import ttag

from django.contrib import auth
#from ..models import SessionAlias
from ..models import InteractivitySession, InteractivityExercise, InteractivityWork

register = template.Library()

@register.inclusion_tag("flash_template.html", name="interactivity")
def do_flash_interactivity():
    '''
    This specifies where in the html body the flash should appear --
    the interactivity_headers tag must be in the header section of the page.
    '''
    return {  }

@register.tag(name="interactivity_header")
class FlashInteractivityHeaders(ttag.Tag):
    '''
    This tag will create all the information for laoding the flash activity and it must appear in the head of the html page,
    then use the interactivity tag in the body.
    '''
    exercise        = ttag.BasicArg()      

    def render(self, context):
        request = context['request']
        data = self.resolve(context)        
        exercise_name = data['exercise']
        
        if not (exercise_name[0] == exercise_name[-1] and exercise_name[0] in ('"', "'")):
            # if there are no quotes, assume that we have been passed a context variable to resolve
            exercise_name = template.Variable(exercise_name).resolve(context)
        else:            
            exercise_name = exercise_name[1:-1]        # strip quotes
       
        exercise = InteractivityExercise.objects.get(name=exercise_name)        
            
        width       = exercise.interactivity.width
        height      = exercise.interactivity.height
        #swf         = 'flash/%s.swf' % application
        swf         = exercise.interactivity.swf.url
        application = os.path.splitext(os.path.basename(swf))[0]

                
        ias = InteractivitySession(                
                session_id  = uuid.uuid4(),
                exercise    = exercise,                
                )
        # user might not be logged in...
        print("=========USER %s  %s" % (context['user'], (context['user'].__class__.__name__)))
        
        print("AUTH?? %s " % (request.user.is_authenticated()))
        if context["user"] != None and context["user"].is_authenticated():
            ias.user = context["user"]
        ias.save()
        
        # get rid of old sessions
        InteractivitySession.objects.delete_old()
        
        interactivityServer     = 'http://%s/interactivity/' % request.META['HTTP_HOST']   # must match path in superactity/urls.py     
#authenticationToken     = _create_auth_token(request)                
        interactivitySessionId  = ias.id  #  NEED TO FIGURE THIS OUT... activity.id
        #resourceTypeId          = "???"
        
        print("NEED TO FIGURE OUT CONDITION")
        #condition           = _get_experimental_condition(context, activity) # figure out if this guy is assigned to condition...
        condition = "alpha"
        
        ## load the header template
        t = template.loader.get_template("flash_header_template.html")
        c = Context({'application':application,
                     'swf':swf,
                     'width':width,
                     'height':height,                     
                     'interactivityServer':interactivityServer,

#NOT AUTHO TOKEN BUT SESSION ID...

                     #'authenticationToken':authenticationToken,                     
                     'interactivitySessionId':interactivitySessionId,
                     #'resourceTypeId':resourceTypeId,
                     'condition':condition,
                     },
                    autoescape=context.autoescape)
        return t.render(c)


def _get_experimental_condition(context, activity):
    """
    If there is an experiment for this activity, figure out which condition the student is in
    """
    request = context['request']
    user = request.user
    
    print('>> get_experimental_condition')
    
    try:
        print('  >> 0')
        ae = SuperActivityExperiment.objects.get(activity=activity)
        print('  >> 1')
        try:
            print('  >> 2')
            # if views or teacher didn't assign during login, asssign now
            at = AssignedTo.objects.get(user=user, experiment=ae)
            
        except:            
            print('  >> 3')
            at = AssignedTo.objects.assign_to_experiment(user, ae)
            
        return at.condition.name    
    
    except:        
        return ''
    

def _assign_condition():
    """
    Eventually, this should qurey the database to see which 
    """
    pass


# def _create_auth_token(request):
#     # generates new 40-char random
#     ss = SessionStore()
#     ss.save()
#     k = ss.session_key
    
#     sa = SessionAlias()
#     sa.alias = k

#     print repr(request.session)
#     #sa.session = Session.objects.get( session_key=request.session.session_key )
#     sa.session = request.session
#     sa.save(); # have to save to generate the key
                
#     # just wanted the key, didn't realy need the session
#     dummy = Session.objects.get(session_key=k);
#     dummy.delete()
    
#     # Matt: not sure why need to set a cookie, ok to just send the alias to flash?
#     # generates new 40-char random
#     #randomcookie = SessionStore().session_key               
#     #kwargs['extra_context']['randomcookie'] = randomcookie
#     #response = direct_to_template( request, **kwargs )
#     #response.set_cookie( randomcookie, value=alias )
        
#     return sa.alias


def _strip_quotes(arg):
    if not (arg[0] == arg[-1] and arg[0] in ('"', "'")):
        raise template.TemplateSyntaxError("Argument %s should be in quotes" % arg)
    return arg[1:-1]

