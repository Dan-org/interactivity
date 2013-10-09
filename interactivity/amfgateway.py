import pyamf, traceback, datetime, logging, os, mimetypes

from pyamf.flex import ArrayCollection, ObjectProxy
from pyamf.remoting.gateway.django import DjangoGateway

from django.http import HttpResponse
from django.contrib.auth import SESSION_KEY, load_backend
from django.contrib import auth
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

from interactivity.models import *
from interactivity.servervos import *

# tell flash/pyamf how to translate from actionscript to python objects
pyamf.register_class(AttemptResponseVO,                         'edu.nu.mwe.loft.client.servervos.AttemptResponseVO')
pyamf.register_class(BeginSessionResponseVO,                    'edu.nu.mwe.loft.client.servervos.BeginSessionResponseVO')
pyamf.register_class(FileRecordVO,                              'edu.nu.mwe.loft.client.servervos.FileRecordVO')
pyamf.register_class(LoadActivityInstructionsFileResponseVO,    'edu.nu.mwe.loft.client.servervos.LoadActivityInstructionsFileResponseVO')
pyamf.register_class(LoadFileRecordResponseVO,                  'edu.nu.mwe.loft.client.servervos.LoadFileRecordResponseVO')
pyamf.register_class(LoadFileDirResponseVO,                     'edu.nu.mwe.loft.client.servervos.LoadFileDirResponseVO')
pyamf.register_class(LogVO,                                     'edu.nu.mwe.loft.client.servervos.LogVO')
pyamf.register_class(StorageVO,                                 'edu.nu.mwe.loft.client.servervos.StorageVO')
pyamf.register_class(SuperactivityServerResponseVO,             'edu.nu.mwe.loft.client.servervos.SuperactivityServerResponseVO')
pyamf.register_class(UserVO,                                    'edu.nu.mwe.loft.client.servervos.UserVO')



def loadClientConfig(request):
    return "load client config response"

def beginSession(request, auth_token, interactivitysession_id):
    
    """
    Starts a interactivity session and sets credentials so that other commands can be called.
    """
    print('beginSession %s' % request.session.session_key)    
    try:
        a = SessionAlias.objects.get( alias=auth_token )
        session_engine = __import__( settings.SESSION_ENGINE, {}, {}, [''] )
        session_wrapper = session_engine.SessionStore( a.session.session_key )
        
        user_id = session_wrapper.get( SESSION_KEY )
        
        if(user_id != None):
            auth.get_user_model()            
            user = auth.get_user_model().objects.get(id=user_id)
            user.backend='django.contrib.auth.backends.ModelBackend'                
            auth.login( request, user )
        else:
            user = None        
        
        a.delete()
        
        # get the records in the saved work directory
        records = _get_file_records(interactivitysession_id)        
        
        print "records: %s" % records

        # will now get session id from SuperActivitySessiion
        sas = InteractivitySession.objects.get(pk=interactivitysession_id)
                
        if user != None:            
            user = UserVO(auth.get_user_model().objects.get(id=user_id))            
        bsr = BeginSessionResponseVO(None, user, records)
        
        return bsr
    except:
        err = "Begin session FAIL! I don't know why"
        print(err)
        return BeginSessionResponseVO(err, None, None)
    
    

def loadInstructionsFile(request, interactivitysession_id):
    #print('loadInstructionsFile')
    if not _is_authenticated(request):
        # don't fail because anonymous users can still load the instructions
        #return LoadActivityInstructionsFileResponseVO("Load Activity FAIL: Not authenticated", None)
        pass
    
    try:                       
        data = InteractivitySession.objects.get(id=interactivitysession_id).exercise.content
        return LoadActivityInstructionsFileResponseVO(None, data)
    except:
        err = "Load Activity FAIL! I don't know why"
        print(err)
        return LoadActivityInstructionsFileResponseVO(err, None)
    
 
def startAttempt(request, activity_id):    
    print("NOT IMPLEMENTED")    
    pass


def scoreAttempt(request, activity_id, score_id, score_value):    
    print("NOT IMPLEMENTED")
    pass


def scoreAttemptInstructor(request, activity_id, score_id, score_value, attempt_number):
    print("NOT IMPLEMENTED")
    pass


def endAttempt(request, activity_id):
    print("NOT IMPLEMENTED")
    pass



def loadFileDir(request, activity_id):    
    """
    Return information about all the files for the given loft/activity/user (if any).
    """
    print('loadFileDir')
    if not _is_authenticated(request):
        return LoadFileDirResponseVO("Load File Dir FAIL: Not authenticated", None)
    
    try:        
        records = _get_file_records(activity_id)
        # send to interactivity
        response = LoadFileDirResponseVO(None, records)        
        return response
    except:
        err = "Fail! Don't know why"
        print(err)
        return LoadFileDirResponseVO(err, [])


def loadFileRecord(request, interactivitysession_id, attempt_number, file_name):
    """
    Load a file for the given loft/activity/user/attempt, e.g., the student work for this activity.
    """
    print('loadFileRecord')
    if not _is_authenticated(request):
        return LoadFileRecordResponseVO("Load File Record FAIL: Not authenticated", None)
    try:                
        ias = InteractivitySession.objects.get(id=interactivitysession_id)
        data = ias.get_work(attempt_number)
        response = LoadFileRecordResponseVO(None, data.content)
        #print " data: %s" % data.content
        return response
    except IOError as e:
        err = "LoadFileRecord could not open file %s" % path
    except:        
        err = "FAIL!  I don't know why"
        
    print(err)
    return LoadFileRecordResponseVO(err, None)


def saveFileRecord(request, interactivitysession_id, attempt_number, file_name, file_data, mime_type):#byte_encoding):
    """
    Save a file for the given loft/activity/user/attempt, e.g., the student work for this activity.
    @deprecated file_name  -- only 1 work file per user/exercise so don't need name
    @depreated mime_type -- only xml for now
    """    
    if not _is_authenticated(request):
        return SuperactivityServerResponseVO("Save File Record FAIL: Not authenticated")

    try:
        ias = InteractivitySession.objects.get(id=interactivitysession_id)        
        #ias.save_file(attempt_number, file_name, file_data, mime_type)
        ias.save_work(attempt_number, file_data)
        return SuperactivityServerResponseVO(None)
    except IOError as e:
        err = "SaveFileRecord could not open file %s" % path
    except BaseException, errMsg:
        err = "SaveFileRecord FAIL!  \n %s \n %s" %  (errMsg, traceback.format_exc())
    print(err)
    #print(errMsg)
    #tb = traceback.format_exc()
    #print(tb)
    return SuperactivityServerResponseVO(err)        


def deleteFileRecord(request, activity_id, attempt_number, file_name):
    """
    Delete the file for the given loft/activitiy/user/attempt, e.g., the student work for this activity
    """
    print('deleteFileRecord')
    if not _is_authenticated(request):
        return SuperactivityServerResponseVO("Delete File Record FAIL: Not authenticated")    
    try:
        InteractivitySession.objects.get(id=interactivitysession_id).delete_file(attempt_number, file_name)        
        return SuperactivityServerResponseVO(None)
    except:
        return SuperactivityServerResponseVO("DeleteFileRecord FAIL! I don't know why")
    


"""
Logging
"""
import xml

def log(request, log_xml):
    """
    Save information about user action in interactivity to database.
    """
    if not _is_authenticated(request):
        return SuperactivityServerResponseVO("Log FAIL: Not authenticated")
    
    print(xml.etree.ElementTree.tostring(log_xml))
    try:
        #should log here...
        #user                = request.user        
        interactivity_session_id = log_xml.attrib.get('interactivity_session_id') # source id is just the activity id        
        ias = InteractivitySession.objects.get(pk=interactivity_session_id)        
        
        action_id           = log_xml.attrib.get('action_id')        
        info_type           = log_xml.attrib.get('info_type')
        #external_object_id  = log_xml.attrib.get('external_object_id')
        info                = log_xml.text
        date_time           = log_xml.attrib.get('date_time')
        timezone            = log_xml.attrib.get('timezone')
        
        date_string = "%s %s" % (date_time, timezone)
        dt = datetime.strptime(date_string, "%Y/%m/%d %H:%M:%S.%f %Z")
        
        #print(">>>> LOG: %s %s %s %s %s" % (interactivity_session_id, action_id, info_type, info, dt))            
        
        actionlog = ActionLog(#user=user,
                              #activity=activity,                              
                              session=ias,
                              action_id=action_id,
                              date_time=dt,
                              info_type=info_type,
                              info=info,
                              #external_object_id=external_object_id,                              
                              )
        actionlog.save()
        print("LOG IGNORED SUPPLEMENTS!")
#        return SuperactivityServerResponseVO(None)
    except BaseException, errMsg:
        err = "Log FAIL!  \n %s \n %s" %  (errMsg, traceback.format_exc())
        print(err)
        #return SuperactivityServerResponseVO("Log FAIL! I don't know why")


"""
Private
"""


def _get_file_records(interactivitysession_id):
    #print "getting file records"
    records = []
    try:
        ias = InteractivitySession.objects.get(id=interactivitysession_id)
        for work in ias.get_all_work(): 
            #print "  work: %s  %s  %s" % (work, work.attempt, work.created_date)
            fr = FileRecordVO(work.attempt, 'saved_work', '?', work.created_date, 'application/xml')
            #print "  fr: %s" % fr
            records.append(fr)    
        #print "  records: %s" % records
        return records
    except:
        err = "_get_file_records Fail! Don't know why"
        return None    
    
def _is_authenticated(request):
    return request.user.is_authenticated()
        
        
def hello(request):
    '''
    For testing that gateway is working.
    '''
    return "Hello"

services = {
    'interactivity.loadClientConfig':loadClientConfig,
    'interactivity.beginSession':beginSession,
    'interactivity.loadInstructionsFile':loadInstructionsFile,   
    'interactivity.startAttempt':startAttempt,
    'interactivity.scoreAttempt':scoreAttempt,
    'interactivity.scoreAttemptInstructor':scoreAttemptInstructor,   
    'interactivity.endAttempt':endAttempt,
    'interactivity.loadFileDir':loadFileDir,
    'interactivity.loadFileRecord':loadFileRecord,
    'interactivity.saveFileRecord':saveFileRecord,
    'interactivity.deleteFileRecord':deleteFileRecord,
    
    #logging
    'interactivity.log':log,
    
    # hellow world
    'interactivity.hello':hello,
}

logging.basicConfig(
    #level=logging.DEBUG,
    #level=logging.INFO,
    #level=logging.WARNING,
    #level=logging.ERROR,
    level=logging.CRITICAL,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

interactivityGateway = DjangoGateway(services, expose_request=True, debug=True, logger=logging,)
