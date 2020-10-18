from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render

class IndexView(generic.ListView):
	template_name = 'bbva/index.html'
	context_object_name = 'index'

	def get_queryset(self):
		return User.objects.all()

class CreditoView(generic.ListView):
	template_name = 'bbva/credito.html'
	context_object_name = 'solicita credito'

	def get_queryset(self):
		return User.objects.all()

class ConsultaView(generic.ListView):
	template_name = 'bbva/consuta.html'
	context_object_name = 'consulta'

	def get_queryset(self):
		return User.objects.all()

class ResultadoView(generic.ListView):
	template_name = 'bbva/resultado.html'
	context_object_name = 'resultado'

	def get_queryset(self):
		return User.objects.all()
