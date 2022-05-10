from django.shortcuts import redirect, render
# Create your views here.
from .models import Room, Topic
from .forms import FormRoom

# example of rnder python list

rooms = [
    {"name":"math","id":2},
    {"name":"science","id":5},
    {"name":"japanese","id":8},
]



def home(request):

    # get the query parameter from the url 
    q = request.GET.get('q')

    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics
    }
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
            # save to db

            # redirect to the home page after send 
            return redirect('/')
    else:
        form = FormRoom()
    
    return render(request,'base/room_form.html',{'form':form})


# update a room view form 
def update_room(request,pk):
    # pk = room that we will update 
    room = Room.objects.get(id = pk)

    if request.method == 'POST':
        form = FormRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        # get a instance of the form from the room to update.
        form = FormRoom(instance=room)      

    return render(request,'base/room_form.html',{'form':form})

def delete_room(request,pk):
    # pk = room we have to delete 
    room  = Room.objects.get(id = pk)
    if request.method =='POST':
        room.delete()
        return redirect('home')
    else:
        return render(request,'base/room_delete.html', {'obj': room} )

            


