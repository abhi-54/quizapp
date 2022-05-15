from django import forms
from django.contrib import admin
from questions.admin import AnswerInline
from questions.models import Answer, Question

class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = '__all__'

class AnswerForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = '__all__'
    extra = 4