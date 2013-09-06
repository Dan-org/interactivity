import os, mimetypes, sys
from datetime import datetime, timedelta
from xml.etree import ElementTree

from django.db import models
from django.core.files import File
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import sessions
from django.core.files.storage import *
from django.core.files.storage import FileSystemStorage

from django import forms
from django.template import Template, Context

# DON"T IMPORT because coflicts with Session in loftmodels.py
#from django.contrib.sessions.models import Session 

from django.conf import settings
from django.contrib import auth

"""
Used to authentical flash interactivity.

The purpose of the interactivity app is to allow flash programs to communicate with the django backend
so that the flash program can save and load files and log user actions.  This requires being able to create an authenticate sessions.

Example of how to authenticate flash app
 http://stackoverflow.com/questions/3553376/flash-pyamf-django-session-cookie-security
"""



class Interactivity(models.Model):
    '''
    A flash activity that can save work to the loft and log user interactions.
    '''
    name    = models.CharField(max_length=255, unique=True)
    swf     = models.FileField(upload_to="interactivities")
    width   = models.IntegerField()
    height  = models.IntegerField()
    
    def __repr__(self):
        return self.name

    def __unicode__(self):
        return repr(self)
    
    
class InteractivityExercise(models.Model):
    """
    Specifies any initial information needed to start the superactivity, e.g., the instructions.
    """    
    interactivity  = models.ForeignKey(Interactivity, related_name="exercises");    
    name           = models.CharField(max_length=255, unique=True)
    content        = models.TextField()    #xml content
    
    # need to have number of attempts here....

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return repr(self)


class InteractivityWork(models.Model):
    """
    Represents students saved work after using interactivity.
    """
    user            = models.ForeignKey(settings.AUTH_USER_MODEL);    
    exercise        = models.ForeignKey(InteractivityExercise)
    attempt         = models.IntegerField(default=0)
    created_date    = models.DateTimeField(auto_now_add=True)
    saved_date      = models.DateTimeField(auto_now_add=True)
    completed       = models.BooleanField(default=False)
    content         = models.TextField(blank=True)    #xml content
    
    def __repr__(self):
        return "InteractivityWork(%r)" % (self.id)

    def __unicode__(self):
        return repr(self)

    
class SessionAlias(models.Model):
    """
    Save an alias to the session so that we can send the alias to flash without showing the session
    """
    alias   = models.CharField( max_length=40, primary_key=True )
    session = models.ForeignKey( sessions.models.Session )
    created = models.DateTimeField( auto_now_add=True )


class InteractivitySessionManager(models.Manager):
    
    def delete_old(self):
        """
        Gets all the conditions for the given experiment
        """
        how_many_days = 1
        old = InteractivitySession.objects.filter(created__lt=datetime.now()-timedelta(days=how_many_days))
        old.delete()


class InteractivitySession(models.Model):
    """
    Session encapsulates a user and exercise so we can refer to both with a single token/id
    """
    created     = models.DateTimeField( auto_now_add=True )    
    session_id  = models.CharField( max_length=40)  # UUID of session.  Should only be 32 chars    
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null = True)    
    exercise    = models.ForeignKey(InteractivityExercise)
    #attempt     = models.IntegerField(default=0)    # right now this isn't set...
    
    objects = InteractivitySessionManager()

    def get_all_work(self):
        works = InteractivityWork.objects.filter(user=self.user, exercise=self.exercise).order_by('attempt')
        return works
    
    def get_work(self, attempt):
        work = InteractivityWork.objects.get(user=self.user, exercise=self.exercise, attempt=attempt)
        return work
    
    def save_work(self, attempt, content):
        print("saving work...")
        print("saving work... %s %s %s" % (self.user, self.exercise, attempt))
        work, created = InteractivityWork.objects.get_or_create(user=self.user, exercise=self.exercise, attempt=attempt)
        print("work... %s" % work)
        work.content = content
        work.save()


"""
The Logging classes allows the loft and its superactivities to track user behavior.
    The ActionLog is the main logging object that has an action and some associated info
    The SupplementLog allows you to next additional information on an actionlog
"""

class ActionLog(models.Model):
    """
    The ActionLog records some user activity from the loft of interactivity and an optional associated bit of data, usually XML.
    """    
    session             = models.ForeignKey(InteractivitySession)
    #user                = models.ForeignKey(User)                                   # link action log to particular user, activity and session
    #session_id          = models.CharField(max_length=50)                           # session_id: optionally provided by loft for grouping by logging session
        
    # information related to the action
    action_id           = models.CharField(max_length=50)                           # action_id: identifes the type of action (e.g. START_ATTEMPT)
    date_time           = models.DateTimeField()                                    # date_time: timestamp for action
    info_type           = models.CharField(max_length=50, blank=True, null=True)       # type of data stored in the info field (e.g. xml)
    info                = models.TextField(blank=True, null=True)                   # all relevant data associated with the action (most likely in XML format)
    #external_object_id  = models.CharField(max_length=50,blank=True, null=True)     # external_object_id: id of the object affected by the action within the application (e.g. window1/frame1/textbox1)
                                                                                    # NOTE: external_object_id does not neccessarily correspond to a content file identifier, it is more like a 'container' in Ken's usage of the term   
    def __unicode__(self):
        return u"ActionLog" 
    

class SupplementLog(models.Model):
    """
    The intent is to nest supplemental information within an action.  These are tied to the parent action in the data.
    Ex: Quiz question responses and scores would be stored as supplemental data, underneath a QUIZ_SUBMIT action	
    """
    actionlog  = models.ForeignKey(ActionLog)
    action_id  = models.CharField(max_length=50)                       # action_id: identifes the type of action (e.g. START_ATTEMPT)
    info_type  = models.CharField(max_length=50)   # type of data stored in the info field (e.g. xml)
    info       = models.TextField(blank=True, null=True)               # all relevant data associated with the action (most likely in XML format)
    
    def __unicode__(self):
        return u"SupplementLog" 


