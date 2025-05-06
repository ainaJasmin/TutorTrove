from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        exclude = ['user']


class TutorSubjectForm(ModelForm):
    class Meta:
        model = TutorSubject
        fields = '__all__'
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

