"""
Server responses
"""

class AttemptResponseVO(object):
    """
    Reponse to startAttempt, scoreAttempt, ScoreAttemptInstructor, EndAttempt
    """
    def __init__(self, errorMessage, current_attempt, max_attempts):
        self.name               = _get_success_message(errorMessage is None)
        self.message            = errorMessage
        self.current_attempt    = current_attempt
        self.max_attempts       = max_attempts   


class BeginSessionResponseVO(object):
    """
    Reponse to BeginSession
    """
    #def __init__(self, errorMessage, user, session_key, file_records):
    def __init__(self, errorMessage, user, file_records):
        self.name       = _get_success_message(errorMessage is None)
        self.message    = errorMessage
        self.user       = user
        #self.session_id = session_key        
        self.storage    = StorageVO(file_records)
        

class FileRecordVO(object):
    def __init__(self, attempt, name, size, created_time, mime_type):
        ##fs = FileSystemStorage(ACTIVITY_MEDIA_ROOT)
        #file name should be relative to file system root
        #rel_path = os.path.join(loft_id, user_id, activity_id, attempt, file_name)        
        # guid - this is the id of the file? or the name?
        # version_number -  ??? not sure what this is        
        #self.loft_guid   = loft_id
        #self.user_guid      = user_id
        #self.activity_guid  = activity_id        
        self.attempt        = attempt
        self.file_name      = name 
        self.file_size      = size 
        self.created_time   = created_time 
        self.mime_type      = mime_type


class LoadActivityInstructionsFileResponseVO(object): 
    """
    Reponse to LoadActivityInstructionsFile
    """
    def __init__(self, errorMessage, file_data):
        self.name           = _get_success_message(errorMessage is None)
        self.message        = errorMessage
        self.instructions   = file_data


class LoadFileDirResponseVO(object):
    """
    Respond to LoadFileDir
    """
    def __init__(self, errorMessage, file_records):
        self.name           = _get_success_message(errorMessage is None)
        self.message        = errorMessage
        self.file_records   = file_records


class LoadFileRecordResponseVO(object):
    def __init__(self, errorMessage, content):
        self.name       = _get_success_message(errorMessage is None)
        self.message    = errorMessage
        self.content    = content
 

class LogVO(object):
    def __init__(self, xml):
        self.xml = xml


class StorageVO(object):
    """
    Holds file directory records
    """
    def __init__(self, file_records):
        self.file_directory = file_records        


class SuperactivityServerResponseVO(object):
    """
    Reponse to Simple commands like save, delete
    """
    def __init__(self, errorMessage):
        self.name    = _get_success_message(errorMessage is None)
        self.message = errorMessage        


class UserVO(object):
    def __init__(self, user):
        self.id         = user.id
        self.full_name  = user.get_full_name()
        #self.first_name = user.first_name
        #self.last_name  = user.last_name


def _get_success_message(is_success):
    """
    Create the success message
    """
    if is_success:
        return "success"
    else:
        return "super_activity_exception"
    