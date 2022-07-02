from django.shortcuts import render,reverse,redirect
from .forms import QuizRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def register(request):
    if request.method == "POST":
        user = QuizRegisterForm(request.POST)
        if user.is_valid():
            user.save()
            return HttpResponse("WELCOME")
        else:
            return render(request, "Accounts/register.html", context={"form": user})
    else:
        form = QuizRegisterForm()
        return render(request, "Accounts/register.html", context={"form": form})


def login(request):
    if request.method == "POST":
        AuthenticationForm(request.POST)
        return HttpResponse(f"hello and welcome{request.user}")
    else:
        form = AuthenticationForm()
        return render(request,"Accounts/login.html",context={"form": form})