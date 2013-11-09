from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib import auth
from django.conf import settings
from django.http import Http404

from interactivity.models import InteractivityExercise, InteractivityWork
from lxml import etree

from models import PolicyworldWork, StageGrade

def home(request):
	exercises = InteractivityExercise.objects.all()
	return render(request, 'policyworld/home.html', locals())

def exercise(request, id):
    #studios = Studio.objects.all()
    
    # get exercise with the given id
    exercise = InteractivityExercise.objects.get(pk=id)
    # eventually, should only get users in given studio
    
    # get all saved work for this exercies
    rows = []

    for work in InteractivityWork.objects.filter(exercise=exercise):
    	agrade = grade(work)
    	row = GradeRow(work, agrade)
    	rows.append(row)

    return render(request, 'policyworld/exercise.html', locals())


def work(request, id):
    #studios = Studio.objects.all()
    
    # get work with the given id
	work = InteractivityWork.objects.get(pk=id)
    # eventually, should only get users in given studio       
	policyworldwork = grade(work)
	return render(request, 'policyworld/work.html', locals())



class GradeRow(object):
    def __init__(self, work, grade):
        self.work = work
        self.grade = grade



def grade(exercise):
    """
    Use the savedWorld.xml file to grade a policy world exercise.
    """
    data = exercise.content
    xml = get_xml(data)        
    pw = analyze_work(xml)
    #g = pw.to_grade()
    #print("GRADE %s" % g)
    #return g
    return pw


def get_xml(saved_work_data):
    """
    Given the data from savedWork.xml file, parses the xml using lxml
    """
    parser = etree.XMLParser(strip_cdata=False)

    saved_work_data = saved_work_data.replace('<?xml version="1.0" encoding="UTF-8"?>', '')

    #print saved_work_data
    # print saved_work_data.encode('ascii', 'ignore')
    save_xml = etree.XML(saved_work_data, parser)
    return save_xml
                    
                    
def analyze_work(policyworld_xml):
    stages = []
    
    for stage_attempts_node in policyworld_xml.findall(".//stageAttempts"):
        name = stage_attempts_node.attrib.get("name")
        #if name in ["pretest", "problem1", "problem2", "problem3", "debateTest", "posttest"]:
        i = 1

        attempts = stage_attempts_node.findall("stageAttempt")
        for stage_attempt_node in attempts:
            completed   = stage_attempt_node.attrib.get("completed") == 'true'
            passed      = stage_attempt_node.attrib.get("passed") == 'true'
            msec        = int(stage_attempt_node.attrib.get("msec"))
            attempt     = i
            i = i+1
                
            stages.append(StageGrade(name, attempt, completed, passed, msec))
                
    pw = PolicyworldWork(stages)
    return pw
