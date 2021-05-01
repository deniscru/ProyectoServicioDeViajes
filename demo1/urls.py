from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('usuario/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
]