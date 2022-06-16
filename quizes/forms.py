from dataclasses import fields
from django import forms
from .models import Subjects1, Quiz

class SubjectForm(forms.ModelForm):
  class Meta: 
    model = Subjects1
    fields = "__all__"

class QuizForm(forms.ModelForm):
  class Meta:
    model = Quiz
    fields = "__all__"