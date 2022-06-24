from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import FormRoom

def register_page(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # get the user before save for update fields(lowerCase).
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            messages.success(request,'Account created successfully')
            return redirect('home')
            """
                NO need it for check if user already exist, Django handdle it in User Model
                with error : " A user with that username already exists "
            """
    
    else:
        form = UserCreationForm()

    context = { "form": form}
    return render(request,'base/login_page.html',context)

def loginPage(request):
    page = 'login'

    """
    if use is already been login in, redirect to home page/ 
    """
    if request.user.is_authenticated:
        return redirect('home')


    # get the values after submit the form.
    # username and password
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # check if user exist, if not , return a message " user does not exist "
        try:
            user = User.objects.get(username = username)

        except:
            messages.error(request, "User does not exist")
            return redirect('login')
        
        
        
        # if user exist , veryfried credentials

        user = authenticate(request, username = username, password = password)

        if user:
            login(request, user)
            print(request.POST)
            return redirect('home')
        else:
            messages.error(request , "Username or Password does not exist" )


    
    context = { "page" : page}
    return render(request,'base/login_page.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):

    # get the query parameter from the url 
    # Q allos to make custom queryies with 'and' or 'or'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__contains = q) | 
        Q(description__icontains = q) |
        Q(host__username__contains = q)

    )
    topics = Topic.objects.all()

    # get many rooms available from last query instance(room)
    room_count = rooms.count() 

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count
    }
    return render(request,'base/home.html',context)

def room(request,id):
    room = Room.objects.get(id = id)
    #-(crated) newest will be first.
    messages = room.message_set.all().order_by('-created')

    # if user write a new messge.
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body = request.POST.get('body')
        )
        return redirect('room', id = room.id)

    context = { 
        'room':room,
        'messages': messages 
     }
    return render(request,'base/room.html', context)

@login_required(login_url='login')
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
@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_room(request,pk):
    # pk = room we have to delete 
    room  = Room.objects.get(id = pk)
    if request.method =='POST':
        room.delete()
        return redirect('home')
    else:
        return render(request,'base/room_delete.html', {'obj': room} )

            


