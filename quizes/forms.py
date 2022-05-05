from django import forms
from .models import Subjects1

class SubjectForm(forms.ModelForm):
  class Meta: 
    model = Subjects1
    fields = "__all__"