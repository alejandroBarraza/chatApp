"""
    base url app go here!
"""

from django.urls import path
from . import views

urlpatterns = [
    # GET REQEUST
    path('',views.home,name='home'),
    path('room/<str:id>/',views.room,name='room'),

    # POST REQUEST
    path('create-room/',views.create_room,name='create-room'),

    # PUT REQUEST 
    path('update-room/<str:pk>/', views.update_room, name = 'update-room'),

    # DELETE REQUEST
    path('delete-room/<str:pk>/', views.delete_room, name = 'delete-room')


]
