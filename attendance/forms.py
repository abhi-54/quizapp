from django import forms
from django.forms.models import ModelForm
from regester.utils import stdchoice

class standardForm():
  std = forms.ChoiceField(choices=stdchoice, required=True)
  class Meta:
    fields = ('std',)