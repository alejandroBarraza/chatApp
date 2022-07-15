import imp
from django.urls import path
from . import views

# base url from api: api/
urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms)
]
