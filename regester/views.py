from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import FormRegestration, ProfileForm, PasswordReset
from .models import profile1
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.views import PasswordChangeDoneView
from django.core.mail import send_mail

# Create your views here.

def landing_page(request):
    return render(request, 'landing/landing_page.html')

def about_page(request):
    return render(request, 'landing/about.html')

def contact_page(request):
  # for sending inquiry (contact us form)
  if request.method == 'POST':    # when user clicks on submit
    fullname = request.POST.get('fullname')   # get name from html form
    emailID = request.POST.get('emailID')   # get email from html form
    message = request.POST.get('message')   # get message from html form
    
    # smtp python's send mail function:
    send_mail(
      'Quiz Web App Query from ' + fullname,  # subject
      message + '\nFrom - ' + emailID,    # message
      emailID,    # by whom (from)
      ['abhipokharkar54@gmail.com',],    # to who
    )
    first_name = fullname.split()
    context = {
      'fullname': first_name[0], 
      'emailID': emailID, 
      'message': message
    }
    return render(request, 'landing/contact.html', context)
  return render(request, 'landing/contact.html')

@login_required
def profile_view(request):
    if request.method == "GET":
        form = ProfileForm()
        user = request.user
        context={
        "form":form
         }
        profile = profile1.objects.get(user=user)
        #print('len', len(profile))
        std = profile.get_std()
        ref_code = profile.get_ref_code()
        if std != '' or std != None:
            context = {
                'std': std,
                'profile': ref_code,
            }
            return render(request, 'already_profile.html', context)
        #print('data: ', std)
        return render(request, "profile.html",context)
    elif request.method == "POST":
        try:
            print(request.POST)
            form = ProfileForm(request.POST)
            post = request.POST
            save1 = profile1()
            save1.user = request.user
            save1.std = post["std"]
            save1.save()
            context={
            "form":form,
            "std": post["std"],
            }
            return render(request, "profile.html",context)
        except IntegrityError:
            context = {
                'std': profile1().std
            }
            return render(request, 'already_profile.html', context)

def reges(request):
    if request.method == "GET":
        form = FormRegestration()
        context = {
            "form": form,
        }
        return render(request, "regestration.html", context=context)
    else:
        #print(request.POST)
        form = FormRegestration(request.POST)
        if form.is_valid():
            profile = profile1()
            profile.std = request.POST['std']
            try:
                entered_ref_code = request.POST['enter_ref_code']
            except MultiValueDictKeyError:
                entered_ref_code = None
            try:
                if entered_ref_code != None or entered_ref_code != '':
                    profile_ref = profile1.objects.get(ref_code = entered_ref_code)
                    profile.referred_by = profile_ref.user
                    pre_points = profile_ref.get_reward_points()
                    new_points = int(pre_points) + 10
                    profile1.objects.filter(ref_code = entered_ref_code).update(reward_points = new_points)
            except profile1.DoesNotExist:
                pass
            user = form.save()
            profile.user = user
            profile.save()
            if user is not None:
                return redirect("Login")
        else:
            msg = 'Please correct the entered details!'
            context = {
                "form": form,
                "msg": msg,
            }
            return render(request, "regestration.html", context=context)

def Login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, "Login.html", context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            #print("authenticated", user)
            if user is not None:
                login(request, user)
                return redirect("dashboard-view")
        else:
            context = {
                "form": form
            }
            return render(request, "Login.html", context=context)

def logout(request):
	logout(request)
	return redirect("Login")

@login_required
def pass_set_view(request, id):
    if request.method == "GET":
        username = User.objects.get(id = id)
        if username == request.user:    # when different id is used while logged in
            user = User.objects.get(username = username)
            reset_form = PasswordReset(user = username)
            context = {
                    'reset_form': reset_form,
                    'username': user,
                }
            return render(request, 'pass_set.html', context)
        else:
            return redirect("logout")
    else:
        username = User.objects.get(id = id)
        user = User.objects.get(username = username)
        reset_form = PasswordReset(user = user, data = request.POST)
        if reset_form.is_valid():
            s = reset_form.save()
            if s is not None:
                return redirect('done-set-password-page')
        else:
            context = {
                'reset_form': reset_form,
                'username': user
            }
            return render(request, 'pass_set.html', context)

def done_setting_pass(request):
    return render(request, 'pass_set_done.html')


