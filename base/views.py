from inspect import Attribute
from multiprocessing import context
from django.shortcuts import render
# Create your views here.
from .models import Room

# example of rnder python list

rooms = [
    {"name":"math","id":2},
    {"name":"science","id":5},
    {"name":"japanese","id":8},
]



def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request,'base/home.html',context)

def room(request,id):
    room = Room.objects.get(id = id)
    context = { 'room':room }
    return render(request,'base/room.html', context)

