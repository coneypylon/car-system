from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generateCarMovement, name='generate'),
    path('execute/', views.executeCarMovement, name='execute'),
]