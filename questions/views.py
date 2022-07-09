from multiprocessing import context
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from questions.forms import AnswerForm, QuestionForm
from questions.models import Answer, Question
from quizes.forms import SubjectForm, QuizForm
from django.forms import inlineformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from quizes.models import Quiz, Subjects1

# Create your views here.

@staff_member_required
def custom_admin(request):
  breadcrumbs = (
    ('Home', '/panel/'),
  )
  subjects = len(Subjects1.objects.all())
  quizes = len(Quiz.objects.all())
  questions = len(Question.objects.all())
  context = {
    'breadcrumbs': breadcrumbs,
    'subjects': subjects,
    'quizes': quizes,
    'questions': questions
  }
  return render(request, 'base_quiz_panel.html', context)

@staff_member_required
def add_subject_view(request):
  form = SubjectForm()
  breadcrumbs = (
    ('Home', '/panel/'),
    ('Add Subject', '/panel/add-subject/')
  )
  context = {
    'form': form,
    'breadcrumbs': breadcrumbs,
  }
  if request.method == 'POST':
    form = SubjectForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'add_subject.html', context)

@staff_member_required
def add_quiz_view(request):
  form = QuizForm()
  breadcrumbs = (
    ('Home', '/panel/'),
    ('Add Quiz', '/panel/add-quiz/')
  )
  context = {
    'form': form,
    'breadcrumbs': breadcrumbs
  }
  if request.method == 'POST':
    form = QuizForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'add_quiz.html', context)

@staff_member_required
def add_question_view(request):
  q_form = QuestionForm()
  a_form = inlineformset_factory(Question, Answer, fields='__all__', extra=4, can_delete=False)
  #a_form = AnswerForm()
  breadcrumbs = (
    ('Home', '/panel/'),
    ('Add Question-Answer', '/panel/add-question/')
  )
  context = {
    'q_form': q_form,
    'a_form': a_form,
    'breadcrumbs': breadcrumbs
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

@staff_member_required
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

@staff_member_required
def display_subjects_view(request):
  breadcrumbs = (
    ('Home', '/panel/'),
    ('View Subjects', '/panel/view-subjects/')
  )
  subjects = Subjects1.objects.all()
  context = {
    'breadcrumbs': breadcrumbs,
    'subjects': subjects
  }

  if request.POST:
    data = request.POST
    sID = data['sModel_id']   # Subject Model ID
    sModel = Subjects1.objects.get(id=sID)
    sForm = SubjectForm(request.POST or None, instance=sModel)
    if sForm.is_valid():
      sForm.save()
      msg = f"Subject #{sID} {sModel} changed successfully !!"
    else:
      msg = f"Edit unsuccessful ! Please try again. If problem persists, contact admin."
    context['msg'] = msg

  return render(request, 'view_subjects.html', context)

@staff_member_required
def display_quizes_view(request):
  breadcrumbs = (
    ('Home', '/panel/'),
    ('View Quizes', '/panel/view-quizes/')
  )
  quizes = Quiz.objects.all()
  context = {
    'breadcrumbs': breadcrumbs,
    'quizes': quizes
  }

  if request.POST:
    data = request.POST
    quizID = data['quizModel_id']   # Quiz Model ID
    quizModel = Quiz.objects.get(id=quizID)
    quizForm = QuizForm(request.POST or None, instance=quizModel)
    if quizForm.is_valid():
      quizForm.save()
      msg = f"Quiz #{quizID} {quizModel} changed successfully !!"
    else:
      msg = f"Edit unsuccessful ! Please try again. If problem persists, contact admin."
    context['msg'] = msg
  return render(request, 'view_quizes.html', context)

@staff_member_required
def display_questions_view(request):
  breadcrumbs = (
    ('Home', '/panel/'),
    ('View Questions', '/panel/view-questions/')
  )
  context = {
    'breadcrumbs': breadcrumbs,
  }
  return render(request, 'view_questions.html', context)

@staff_member_required
def display_Allquestions_view(request):
  breadcrumbs = (
    ('Home', '/panel/'),
    ('View Questions', '/panel/view-questions/'),
    ('View All Questions', '/panel/view-questions/all/')
  )
  questions = Question.objects.all()
  context = {
    'breadcrumbs': breadcrumbs,
    'questions': questions
  }
  if request.POST:
    data = request.POST
    questID = data['qModel_id']   # Question ID
    qInstance = Question.objects.get(id=questID)   # Question Model Instance
    Qform = QuestionForm(request.POST or None, instance=qInstance)
    a_form = inlineformset_factory(Question, Answer, fields='__all__', extra=0,can_delete=False)
    if Qform.is_valid():
      created_Qform = Qform.save(commit=False)
      Aform = a_form(request.POST, instance=created_Qform)
      if Aform.is_valid():
        created_Qform.save()
        Aform.save()
        msg = f"Question #{questID} {qInstance} changed successfully !!"
      else:
        msg = f"Edit unsuccessful ! Please try again. If problem persists, contact admin."
      context['msg'] = msg
  
  return render(request, 'allQuestions.html', context)

@staff_member_required
def modify_subject_view(request):
  if request.POST:
    breadcrumbs = (
      ('Home', '/panel/'),
      ('View Subjects', '/panel/view-subjects/'),
      ('Modify Subject', '#')
    )

    data = request.POST
    sID = data['subjectID']   # subject ID
    sModel = Subjects1.objects.get(id=sID)    # Subject Model
    sForm = SubjectForm()

    context = {
      'breadcrumbs': breadcrumbs,
      'sModel': sModel,
      'sForm': sForm
    }
    return render(request, 'modify_subject.html', context)
  return redirect('view-subjects-page')

@staff_member_required
def modify_quiz_view(request):
  if request.POST:
    breadcrumbs = (
      ('Home', '/panel/'),
      ('View Quizes', '/panel/view-quizes/'),
      ('Modify Quiz', '#')
    )

    data = request.POST
    quizID = data['quizID']   # quiz ID
    quizModel = Quiz.objects.get(id=quizID)    # quiz Model
    quizForm = QuizForm()

    subjectIndex = 0
    for index, i in enumerate(Subjects1.objects.all()):
      if i == quizModel.subject:
        subjectIndex = index+1

    context = {
      'breadcrumbs': breadcrumbs,
      'quizModel': quizModel,
      'quizForm': quizForm,
      'subjectIndex': subjectIndex
    }
    return render(request, 'modify_quiz.html', context)
  return redirect('view-quizes-page')

@staff_member_required
def modify_question_view(request):
  if request.POST:
    breadcrumbs = (
      ('Home', '/panel/'),
      ('View Questions', '/panel/view-questions/'),
      ('Modify Question', '#')
    )
    
    data = request.POST
    q = data['question']
    qModel = Question.objects.get(text=q) # Question Model
    q_form = QuestionForm()
    a_form = inlineformset_factory(Question, Answer, fields='__all__', extra=0,can_delete=False)
    formset = a_form(instance=qModel)

    quizes = Quiz.objects.all()
    index = None    # value of <select> of Quiz
    for i, quiz in enumerate(quizes):
      if quiz == qModel.quiz:
        index = i + 1

    i_typeQ = None    # value of <select> of Type of Question
    if 'MCQ' in qModel.type_of_question or '0' in qModel.type_of_question:
      i_typeQ = 0
    else:
      i_typeQ = 1

    context = {
      'breadcrumbs': breadcrumbs,
      'Qform': q_form,
      'a_form': a_form,
      'qModel': qModel,
      'index1': index,
      'index2': i_typeQ,
      'formset': formset
    }
    return render(request, 'modify_question.html', context)
  return redirect('view-questions-page')