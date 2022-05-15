from django.http import HttpResponseRedirect
from django.shortcuts import render
from questions.forms import AnswerForm, QuestionForm
from questions.models import Answer, Question
from quizes.forms import SubjectForm, QuizForm
from django.forms import inlineformset_factory

# Create your views here.

def custom_admin(request):
  return render(request, 'base_quiz_panel.html')

def add_subject_view(request):
  form = SubjectForm()
  context = {
    'form': form
  }
  if request.method == 'POST':
    form = SubjectForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'add_subject.html', context)

def add_quiz_view(request):
  form = QuizForm()
  context = {
    'form': form
  }
  if request.method == 'POST':
    form = QuizForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'add_quiz.html', context)

def add_question_view(request):
  q_form = QuestionForm()
  a_form = inlineformset_factory(Question, Answer, fields='__all__', extra=4, can_delete=False)
  #a_form = AnswerForm()
  context = {
    'q_form': q_form,
    'a_form': a_form
  }
  if request.method == 'POST':
    print(request.POST)
    Qform = QuestionForm(request.POST)
    if Qform.is_valid():
      created_Qform = Qform.save(commit=False)
      Aform = a_form(request.POST, instance=created_Qform)
      if Aform.is_valid():
        created_Qform.save()
        Aform.save()
   
  return render(request, 'add_question.html', context)

def add_answer_view(request):
  form = inlineformset_factory(Question, Answer, fields='__all__', extra=4)
  form = AnswerForm()
  context = {
    'form': form
  }
  if request.method == 'POST':
    form = AnswerForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'add_answer.html', context)
