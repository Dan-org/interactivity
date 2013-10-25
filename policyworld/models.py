from django.db import models
from lxml import etree

PRETEST     = "pretest"
PROBLEM_1   = "problem1"
PROBLEM_2   = "problem2"
PROBLEM_3   = "problem3"
DEBATETEST  = "debateTest"
POSTTEST    = "posttest"


class PolicyworldWork(object):
    def __init__(self, stages):
        self.stages = stages

    def get_stage(self, name):
        for s in self.stages:
            if s.name == name:
                return s
        return None
    
    def get_time(self):
        t = 0
        for s in self.stages:
            t = t + s.get_minutes()
        return t
    
    def to_grade(self):
        #return "%s %s %s %s %s %s time:%s" % (self._passed_to_string(self.get_stage(PRETEST).passed),
        #                                      self._passed_to_string(self.get_stage(PROBLEM_1).passed),
        #                                      self._passed_to_string(self.get_stage(PROBLEM_2).passed),
        #                                      self._passed_to_string(self.get_stage(PROBLEM_3).passed),
        #                                      self._passed_to_string(self.get_stage(DEBATETEST).passed),
        #                                      self._passed_to_string(self.get_stage(POSTTEST).passed),
        #                                      self.get_time())
        return "Pre:%s Post1:%s Post2:%s Time:%s" % (self._grade_stage(PRETEST),
                                                    self._grade_stage(DEBATETEST),
                                                    self._grade_stage(POSTTEST),
                                                    self.get_time())
    def _grade_stage(self, stage_name):
        s = self.get_stage(stage_name)
        if s == None:
            return "?"
        
        if s.passed:
            return '+'
        else:
            return '-'
    
class StageGrade(object):
    def __init__(self, name, attempt, completed, passed, msec):
        self.name       = name
        self.attempt    = attempt
        self.completed  = completed
        self.passed     = passed
        self.msec       = msec
    	self.min       	= msec/60000

    def get_minutes(self):
        return int(float(self.msec)/60000)