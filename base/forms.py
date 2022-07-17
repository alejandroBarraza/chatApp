from dataclasses import field
from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username','email','password1', 'password2']

class FormRoom(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
       

class FormUser(ModelForm):
    class Meta:
        model = User
        fields = [ 'name', 'email', 'bio', 'avatar']



