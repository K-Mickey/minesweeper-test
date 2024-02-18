from django.urls import path

from . import views

urlpatterns = [
    path('new', views.new, name='new'),
    path('turn', views.turn, name='turn'),
]
