from django.urls import path

from . import views

urlpatterns = [
    path('', views.layout, name='index'),
    path('location', views.location, name='newlocation'),
]