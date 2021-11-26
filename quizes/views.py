from django.db import models
from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView

# Create your views here.
class QuizListView(ListView):
  model = Quiz
  template_name = 'quizes/main.html'

def quiz_view(request, pk):
  quiz = Quiz.objects.get(pk = pk)
  dictionary = {'obj': quiz}
  return render(request, 'quizes/quiz.html', dictionary)
