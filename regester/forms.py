
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import profile1
from .utils import stdchoice

class FormRegestration(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=120,required=True)
    last_name = forms.CharField(max_length=120,required=False)
    std = forms.ChoiceField(choices=stdchoice, required=True)
    enter_refferal_code = forms.CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2","std","enter_refferal_code",)

class ProfileForm(ModelForm):
    class Meta:
        model = profile1
        fields = ("std",)

class PasswordReset(SetPasswordForm):
    class Meta:
        model = User
        fields = ("password1", "password2")

