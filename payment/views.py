from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from quizes.models import Subjects1
from regester.models import profile1
from payment.models import quizAccessTable
from django.utils.datastructures import MultiValueDictKeyError

# html pages related to Payment Dashboard are inherited by Custom Admin Panel base template

# Create your views here.
@staff_member_required
def payment_dashboard_view(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Payment Alternative', '/payment/'),
  )
  context = {
    'breadcrumbs': breadcrumbs,
  }
  if request.method == 'POST':
    #print('after-----:', request.POST)
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
    if len(quizAccessTable.objects.filter(user = username)) == 0:   # Assigning subjects for the first time
      quizAccessTable.objects.create(user = username, subjects = strSubjects, std = std)
    elif len(quizAccessTable.objects.filter(user = username)) == 1:   # If the user is already registered with subjects
      quizAccessTable.objects.filter(user = username).update(subjects = strSubjects, std = std)
    #print(username, std)
    msg = f'Subjects allowed successfully for the user @{username}'
    context['msg'] = msg
    return render(request, 'base_payment.html', context)
  return render(request, 'base_payment.html', context)

@staff_member_required
def paymentTemp(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Payment Alternative', '/payment/'),
      ('Select Student', '#')
  )
  msg = ''
  if request.method == 'POST':
    std = request.POST['btn']
    userProfile = profile1.objects.filter(std = std)
    users = []
    stds = []
    tempUserList = [u.username for u in User.objects.filter(is_superuser = False, is_staff = False)]
    for i in userProfile:
      user_name = i.get_username()
      # if the user is present in profile1 table but not in User table:
      if user_name in tempUserList:
        userModel = User.objects.get(username = user_name)
        users.append(userModel)
        stds.append(std)
      else:
        if request.user in User.objects.filter(is_superuser = True, is_staff = True):   # if user is admin
          continue
        else:
          msg += f"Alert! User: @{user_name} is not present in 'User' table. Please create the user in 'User' table or delete the user from 'profile1' table!"   
  else:
    tempProfile1List = [p.user for p in profile1.objects.all()]
    users = User.objects.filter(is_superuser = False, is_staff = False)
    print('----profiles--------', tempProfile1List)
    print('-----User-------', users)
    stds = []
    for i in range(0, len(users)):
      # if the user is present in User table but not in profile1 table:
      if users[i] in tempProfile1List:
        profile = profile1.objects.get(user = users[i].username)
        std = profile.get_std()
        stds.append(std)
      else:
        msg += f"Alert! User: @{users[i]} is not present in 'profile1' table. Please create the user in 'profile1' table or delete the user from 'User' table"
  context = {
    'users': users,
    'stds': stds,
    'title': 'Select Users',
    'breadcrumbs': breadcrumbs,
    'msg': msg,
  }
  return render(request, 'showUsers.html', context)

@staff_member_required
def quizAllow(request):
  breadcrumbs = (
      ('Home', '/panel/'),
      ('Payment Alternative', '/payment/'),
      ('Allow Quiz', '#')
  )
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
    #print(allowed, s.strip(', '))
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
    'breadcrumbs': breadcrumbs,
  }
  return render(request, 'quizAllow.html', context)


    