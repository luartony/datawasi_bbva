from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('credito', views.CreditoView.as_view(), name='credito'),
    path('consulta', views.ConsultaView.as_view(), name='consulta'),
    path('resultado', views.ResultadoView.as_view(), name='resultado'),
]