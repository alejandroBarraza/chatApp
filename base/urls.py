"""
    base url app go here!
"""

from django.urls import path
from . import views

urlpatterns = [
    # Base url
    path('',views.home,name='home'),

    # User url
    path('login/',views.loginPage, name = 'login'),
    path('logout/',views.logoutUser, name= 'logout'),
    path('register/',views.register_page, name = 'register'),
    
    #Room url
    path('room/<str:id>/',views.room,name='room'),
    path('create-room/',views.create_room,name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name = 'update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name = 'delete-room')


]
