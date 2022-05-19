"""
    base url app go here!
"""

from django.urls import path
from . import views

urlpatterns = [
    # GET REQEUST
    path('',views.home,name='home'),
    path('room/<str:id>/',views.room,name='room'),
    path('logout/',views.logoutUser, name= 'logout'),

    # POST REQUEST
    path('create-room/',views.create_room,name='create-room'),
    path('login/',views.loginPage, name = 'login'),

    # PUT REQUEST 
    path('update-room/<str:pk>/', views.update_room, name = 'update-room'),

    # DELETE REQUEST
    path('delete-room/<str:pk>/', views.delete_room, name = 'delete-room')


]
