
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormRegestration(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=120,required=True)
    last_name = forms.CharField(max_length=120,required=False)
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2")
