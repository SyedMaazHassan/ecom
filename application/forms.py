from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# OUR OWN CUSTOM USER REGISTRATION FORM 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']