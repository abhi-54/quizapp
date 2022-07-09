from multiprocessing import context
from attendance.models import attendanceTable
from regester.forms import FormRegestration
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
  stds = stdchoice
  if request.path == '/payment/class/':
    title = 'Payment'
  else:
    title = 'Attendance'
  context = {
      "stds": stds,
      "title": title,
  }
  return render(request, 'select_class.html', context)

def select_subject_view(request):
  if request.method == 'POST':
    std = request.POST['btn']
    subjects = Subjects1.objects.filter(std = std)
    subjects_list = []
    for subject in subjects:
      subjects_list.append(subject.get_subject_name())
    context = {
      'std': std,
      'subjects': subjects_list,
    }
    return render(request, 'select_subject.html', context)
  return redirect('select-class-page')

def mark_attendance_view(request):
  if request.method == 'POST':
    std = request.POST['std']
    subject = request.POST['sub-btn']
    users = profile1.objects.filter(std = std)
    userModel_list = []
    for i in users:
      user_name = i.get_username()
      userModel = User.objects.get(username = user_name)
      userModel_list.append(userModel)
    context = {
      'std': std,
      'users': userModel_list,
      'subject': subject,
    }
    return render(request, 'mark_attendance.html', context)
  return redirect('select-class-page')

def attendace_marked_view(request):
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
      'n_total': len(users)
    }
    return render(request, 'marked.html', context)
  return redirect('select-class-page')