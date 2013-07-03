from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from interactivity.models import InteractivityExercise


def hi(request):
    return render(request, 'interactivity/interactivity.html', locals())

def exercise(request, exercise_id):
    exercise_name = InteractivityExercise.objects.get(pk=exercise_id).name
    return render(request, 'interactivity/exercise.html', locals())
