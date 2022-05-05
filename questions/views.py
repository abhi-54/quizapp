from multiprocessing import context
from django.shortcuts import render
from quizes.forms import SubjectForm

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
      context += {
        
      }
  return render(request, 'add_subject.html', context)


