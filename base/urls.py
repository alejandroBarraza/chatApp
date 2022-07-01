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
    path('delete-room/<str:pk>/', views.delete_room, name = 'delete-room'),


    #Message url
    path('message/delete/<str:pk>/',views.delete_message, name='delete-message'),

    #User url
    path('profile/<str:pk>/', views.profile, name = 'profile'),
    path('profile/edit/<str:username>/', views.edit_profile, name = 'edit-profile')

]
