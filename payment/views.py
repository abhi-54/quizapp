from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from quizes.models import Subjects1
from regester.models import profile1
from payment.models import quizAccessTable
from django.utils.datastructures import MultiValueDictKeyError
from django.db.utils import IntegrityError

# Create your views here.
@staff_member_required
def payment_dashboard_view(request):
  return render(request, 'base_payment.html')

@staff_member_required
def paymentTemp(request):
  if request.method == 'POST':
    std = request.POST['btn']
    userProfile = profile1.objects.filter(std = std)
    users = []
    stds = []
    for i in userProfile:
      user_name = i.get_username()
      userModel = User.objects.get(username = user_name)
      users.append(userModel)
      stds.append(std)
  else:
    users = User.objects.filter(is_superuser = False, is_staff = False)
    stds = []
    for i in range(0, len(users)):
      profile = profile1.objects.get(user = users[i].username)
      std = profile.get_std()
      stds.append(std)
  context = {
    'users': users,
    'stds': stds,
    'title': 'Select Users'
  }
  return render(request, 'showUsers.html', context)

@staff_member_required
def quizAllow(request):
  username = request.POST['btn']
  user = User.objects.get(username = username)
  profile = profile1.objects.get(user = username)
  std = profile.get_std()
  subjects = Subjects1.objects.filter(std = std)
  #print(request.POST)

  # to display subjects which are currently allowed
  try:
    quizA_Table = quizAccessTable.objects.get(user = username)
    allowed = []
    s = str(quizA_Table.subjects)
    allowed.append(s.strip(', '))
    print(allowed, s.strip(', '))
  except quizAccessTable.DoesNotExist:
    allowed = ["No Subjects allowed"]
  context = {
    'username': username,
    'user': user,
    'std': std,
    'subjects': subjects,
    'len_subjects': len(subjects)+1,
    'alreadyAllowed': allowed,
    'len_alreadyAllowed': len(allowed)+1,
  }
  return render(request, 'quizAllow.html', context)

@staff_member_required
def afterSubmit(request):
  if request.method == 'POST':
    print('after-----:', request.POST)
    username = request.POST['user']
    std = request.POST['std']
    len_subjects = request.POST['subjects']
    subjects_to_allow = []
    strSubjects = ""
    for i in range(1,int(len_subjects)+1):
      temp = 'subjects_to_allow_' + str(i)
      try:
        sub = request.POST[temp]
        subjects_to_allow.append(sub)
        strSubjects = strSubjects + sub + ', '
      except MultiValueDictKeyError:
        continue
    if len(quizAccessTable.objects.filter(user = username)) == 0:
      quizAccessTable.objects.create(user = username, subjects = strSubjects, std = std)
    elif len(quizAccessTable.objects.filter(user = username)) == 1:
      quizAccessTable.objects.filter(user = username).update(subjects = strSubjects, std = std)
    print(username, std)
    return redirect('show-users-all')
  return redirect('show-users-all')
    