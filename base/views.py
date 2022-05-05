from django.shortcuts import redirect, render
# Create your views here.
from .models import Room
from .forms import FormRoom

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

def create_room(request):

    # if a post request with the data from the form.
    if request.method == 'POST':
        form = FormRoom(request.POST)
        if form.is_valid():
            # work with the data
            form.save()
    else:
        form = FormRoom()
    
    return render(request,'base/room_form.html',{'form':form})


