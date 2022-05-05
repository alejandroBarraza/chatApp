"""
    base url app go here!
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:id>/',views.room,name='room'),

    #post actions
    path('create-room/',views.create_room,name='create-room')
]
