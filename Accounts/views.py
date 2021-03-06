from django.shortcuts import render, reverse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout, login as django_login
from django.http import HttpResponse
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        user = RegisterForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect("login")
        else:
            return render(request, "Accounts/register.html", context={"form": user})
    else:
        form = RegisterForm()
        return render(request, "Accounts/register.html", context={"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            if request.user.is_student():
                return redirect("quiz-home")
            else:
                return redirect("teacher-panel")
        else:
            return render(request, "Accounts/login.html", context={"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "Accounts/login.html", context={"form": form})


def logout(request):
    django_logout(request)
    return redirect("quiz-home")
