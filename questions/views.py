
from django.shortcuts import redirect, render
from questions.forms import AnswerForm, QuestionForm
from questions.models import Answer, Question
from quizes.forms import SubjectForm, QuizForm
from django.forms import inlineformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from quizes.models import Quiz, Subjects1
from regester.models import profile1
from results.models import Result
from django.contrib.auth.models import User
from quizes.views import get_subjects
from regester.utils import stdchoice

# Create your views here.
@staff_member_required
def api_subjects(request):
  context = {
    'classes': stdchoice,
  }
  return render(request, 'api_subjects.html', context)

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
    subject_name = form['name'].value()
    std = form['std'].value()
    subject_model = Subjects1.objects.filter(std=std, name=subject_name)
    if len(subject_model) >= 1:
      msg = f"Alert! Subject '{subject_name}' already exits in Class '{std}'"
      context['msg'] = msg
    else:
      if form.is_valid():
        form.save()
      else:
        context['form'] = form
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
    else:
      context['form'] = form
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
    Qform = QuestionForm(request.POST)
    if Qform.is_valid():
      created_Qform = Qform.save(commit=False)
      Aform = a_form(request.POST, instance=created_Qform)
      if Aform.is_valid():
        created_Qform.save()
        Aform.save()
      else:
        msg = "Error!"
        context['msg'] = msg
    else:
      msg = "Error!"
      context['msg'] = msg
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
    msg = ''
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

@staff_member_required
def students_view(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Students Profile', '/panel/students/')
    )
  context = {
    'breadcrumbs': breadcrumbs,
  }
  return render(request, 'students.html', context) 

@staff_member_required
def select_student_view(request):
  if request.POST:
    breadcrumbs = (
      ('Home', '/panel/'),
      ('Student Profile', '/panel/student/'),
      ('Select Class', '/panel/student/class/'),
      ('Select Student', '#'),
    )
    std = request.POST['btn']
    students_profile_list = profile1.objects.filter(std=std)
    students_list = []
    for student in students_profile_list:
      result_table = Result.objects.filter(user = student.user)
      student_dictionary = {
        'student': student,   # profile1 object
        'student_results': len(result_table),
      }
      students_list.append(student_dictionary)
    context = {
      'breadcrumbs': breadcrumbs,
      'students_list': students_list,
    }
    return render(request, 'select_student.html', context)
  return redirect('students-class-page')

@staff_member_required
def show_student_info_view(request, id):
  breadcrumbs = (
    ('Home', '/panel/'),
    ('Student Profile', '/panel/student/'),
    ('Select Class', '/panel/student/class/'),
    ('Select Student', '/panel/student/class/select-student/'),
    ('Student Information', '#'),
  )
  user = User.objects.get(id=id)
  profile = profile1.objects.get(user=user)
  result_table = Result.objects.filter(user=user)
  subjects_allowed, std_subjects, not_allowed_subjects, msg_list = get_subjects(user.username)
  context = {
    'breadcrumbs': breadcrumbs,
    'result_table': result_table,
    'subjects_allowed': subjects_allowed,
    'std_subjects': std_subjects
  }
  return render(request, 'student_info.html', context)

# this function is not used
def display_summary(request, id):
  breadcrumbs = (
    ('Home', '/panel/'),
    ('Student Profile', '/panel/student/'),
    ('Select Class', '/panel/student/class/'),
    ('Select Student', '/panel/student/class/select-student/'),
    ('Student Information', '#'),
  )
  result_table = Result.objects.get(id=id)
  user = User.objects.get(username=result_table.user)
  profile = profile1.objects.get(user=user)
  result_tables = Result.objects.filter(user=user)
  subjects_allowed, std_subjects, not_allowed_subjects, msg_list = get_subjects(user.username)
  

  # ------------------------------------
  result_table = Result.objects.get(id=id)
  summary = result_table.result_summary   # dictionary
  
  questions = []
  correct_answers = []
  answered = []
  if summary != None or summary == '':
    for k, v in summary.items():
      questions.append(k)
      correct_answers.append(v['correct_answer'])
      answered.append(v['answered'])
  context = {
    'breadcrumbs': breadcrumbs,
    'result_table': result_tables,
    'subjects_allowed': subjects_allowed,
    'std_subjects': std_subjects,
    'questions': questions,
    'correct_answers': correct_answers,
    'answered': answered
  }
  return render(request, 'display.html', context)
