from multiprocessing import context
from attendance.models import attendanceTable
from django.shortcuts import redirect, render
from quizes.models import Subjects1
from regester.models import profile1
from regester.utils import stdchoice
from django.contrib.auth.models import User
import datetime
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@staff_member_required
def select_class_view(request):
  print(request.path)
  if request.path == '/payment/class/':  
    breadcrumbs = (
      ('Home', '/panel/'),
      ('Payment Alternative', '/payment/'),
      ('Select Class', '/payment/class/'),
    )
    title = 'Payment'
  elif request.path == '/attendance/class/':
    breadcrumbs = (
      ('Home', '/panel/'),
      ('Attendance - Select Class', '/attendance/class/'),
    )
    title = 'Attendance'
  elif request.path == '/panel/student/class/':
    breadcrumbs = (
      ('Home', '/panel/'),
      ('Student Profile', '/student/'),
      ('Select Class', '/student/class/'),
    )
    title = 'Student Profiles'
  stds = stdchoice  
  context = {
      "stds": stds,
      "title": title,
      "breadcrumbs": breadcrumbs,
  }
  return render(request, 'select_class.html', context)

def select_subject_view(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Attendance - Select Class', '/attendance/class/'),
      ('Select Subject', '#'),
  )
  if request.method == 'POST':
    std = request.POST['btn']
    subjects = Subjects1.objects.filter(std = std)
    subjects_list = []
    for subject in subjects:
      subjects_list.append(subject.get_subject_name())
    context = {
      'std': std,
      'subjects': subjects_list,
      "breadcrumbs": breadcrumbs,
    }
    return render(request, 'select_subject.html', context)
  return redirect('select-class-page')

def mark_attendance_view(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Attendance - Select Class', '/attendance/class/'),
      ('Select Subject', '/attendance/class/subject/'),
      ('Mark Attendance', '#'),
  )
  if request.method == 'POST':
    std = request.POST['std']
    subject = request.POST['sub-btn']
    users = profile1.objects.filter(std = std)
    userModel_list = []
    msg = ''
    for i in users:
      user_name = i.get_username()
      print('------', user_name)
      userModel = User.objects.get(username = user_name)
      userModel_list.append(userModel)
      
    context = {
      'std': std,
      'users': userModel_list,
      'subject': subject,
      'msg': msg,
      "breadcrumbs": breadcrumbs,
    }
    return render(request, 'mark_attendance.html', context)
  return redirect('select-class-page')

def attendace_marked_view(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Attendance - Select Class', '/attendance/class/'),
      ('Select Subject', '/attendance/class/subject/'),
      ('Mark Attendance', '/attendance/class/subject/user/'),
      ('Marked', '#'),
  )
  if request.method == 'POST':
    date1 = request.POST['date']
    date = datetime.datetime.strptime(date1, '%d/%m/%Y').strftime('%Y-%m-%d')
    print(date1, date)
    subject = request.POST['subjects']
    std = request.POST['std']
    data = request.POST
    data_ = dict(data.lists())
    data_.pop('csrfmiddlewaretoken')
    data_.pop('date')
    data_.pop('subjects')
    data_.pop('std')

    users_present = list(data_.keys())  # total students 'present' 
    userModel_present_list = []
    for user in users_present:
      userModel_present = User.objects.get(username = user)
      userModel_present_list.append(userModel_present)
    
    users = profile1.objects.filter(std = std)  # total students in class
    for i in users:
      user_name = i.get_username()
      userModel = User.objects.get(username = user_name)
      if userModel in userModel_present_list:
        attendanceTable.objects.create(user = userModel, course_name = subject, date = date, attendance = 'Present')
      else:
        attendanceTable.objects.create(user = userModel, course_name = subject, date = date, attendance = 'Absent')
    context = {
      'std': std,
      'date': date,
      'subject': subject,
      'n_present': len(userModel_present_list),
      'n_total': len(users),
      "breadcrumbs": breadcrumbs,
    }
    return render(request, 'marked.html', context)
  return redirect('select-class-page')