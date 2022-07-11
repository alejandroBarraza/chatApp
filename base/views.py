from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import FormRoom, FormUser

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
            return redirect('home')
        else:
            messages.error(request , "Email or Password does not exist" )


    
    context = { "page" : page}
    return render(request,'base/login_page.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def profile(request,pk):
    
    user = User.objects.get(pk = pk)
    topics = Topic.objects.all()
    #rooms that the user create.
    rooms = user.room_set.all()
    activity_feed = user.message_set.all().order_by('-created')[:5]
    context = {
        'user': user,
        'topics': topics,
        'rooms': rooms,
        'activity_feed' : activity_feed
    }
    return render(request,'base/user_profile.html',context)

@login_required(login_url='login')
def edit_profile(request,username):

    user = request.user
    if user.username != username:
        return HttpResponse("Your are not allowd to edit this user.")

    if request.method == "POST":
        form = FormUser(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk = user.id)
        

    else:
        form = FormUser(instance = user)
        context = {
            'user':user,
            'form':form
        }
        

    return render(request,'base/edit-profile.html', context)


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
    topics = Topic.objects.all()[0:5]

    # get many rooms available from last query instance(room)
    room_count = rooms.count() 

   
    #get activity feed.
    # activity_feed = Message.objects.all().order_by('-created')[:5]
    activity_feed = Message.objects.filter(room__topic__name__icontains = q)

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'activity_feed': activity_feed 
    }
    return render(request,'base/home.html',context)

def room(request,id):
    room = Room.objects.get(id = id)
    #-(crated) newest will be first.
    room_messages = room.message_set.all().order_by('-created')
    room_participants = room.participants.all()
    # if user write a new messge.
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body = request.POST.get('body')
        )
        # if user send a message to a room that is not joined,add it.
        room.participants.add(request.user)
        
        
        return redirect('room', id = room.id)

    context = { 
        'room':room,
        'room_messages': room_messages,
        'room_participants':room_participants
     }
    return render(request,'base/room.html', context)

@login_required(login_url='login')
def create_room(request):

    # if a post request with the data from the form.
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    else:
        form = FormRoom()
        context = {
            'topics': topics,
            'form': form
        }
        
    return render(request,'base/room_form.html', context)


# update a room view form 
@login_required(login_url='login')
def update_room(request,pk):
    # pk = room that we will update 
    room = Room.objects.get(id = pk)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("Your are not allowed to edit this room.")

    if request.method == 'POST':
        topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description') 
        room.save()
        return redirect('home')

    else:
        # get a instance of the form from the room to update.
        form = FormRoom(instance=room)    


    return render(request,'base/room_form.html',{'form':form,'topics':topics,'room':room})

@login_required(login_url='login')
def delete_room(request,pk):
    # pk = room we have to delete 
    room  = Room.objects.get(id = pk)
    if request.method =='POST':
        room.delete()
        return redirect('home')
    else:
        return render(request,'base/delete.html', {'obj': room} )



# messages 
def delete_message(request,pk):

    message = Message.objects.get(id = pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    else:
        return render(request,'base/delete.html', {'obj': message} ) 
    

# Mobile
def mobile_topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter( name__icontains = q)
    context = {'topics':topics}
    return render(request,'base/topics.html',context)
 

def mobile_activity(request):
    
    room_messages = Message.objects.all()[0:5]
    return render(request, 'base/activity.html', {'room_messages': room_messages})




