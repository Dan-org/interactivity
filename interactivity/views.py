from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from interactivity.models import Interactivity, InteractivityExercise


def exercise(request, exercise_id):
    exercise_name = InteractivityExercise.objects.get(pk=exercise_id).name
    return render(request, 'interactivity/exercise.html', locals())

@staff_member_required
def all_interactivities(request):
	interactivities = Interactivity.objects.all()
	return render(request, 'interactivity/all_interactivities.html', locals())




from pyamf.remoting.client import RemotingService
import logging

def hello(request):
	logging.basicConfig(
    	level=logging.DEBUG,
		format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
	)
	gw = RemotingService('http://127.0.0.1:8000/interactivity/', logger=logging)
	service = gw.getService('interactivity')
	output = service.hello()
    #print output
	return render(request, 'interactivity/hello.html', locals())