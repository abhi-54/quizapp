from django.contrib.auth import authenticate, login,logout

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import FormRegestration
# Create your views here.

def reges(request):
    if request.method == "GET":
        form = FormRegestration()
        context = {
            "form": form,
        }
        return render(request, "regestration.html", context=context)
    else:
        print(request.POST)
        form = FormRegestration(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect("Login")
        else:
            context = {
                "form": form,
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
            print("authenticated", user)
            if user is not None:
                login(request, user)
                return redirect("main-view")

        else:
            context = {
                "form": form
            }
            return render(request, "Login.html", context=context)