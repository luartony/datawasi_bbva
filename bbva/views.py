from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render

class IndexView(generic.ListView):
    template_name = 'bbva/index.html'
    context_object_name = 'latest_question_list'
    

    def get_queryset(self):
    	"""Return the last five published questions."""
    	return User.objects.all()