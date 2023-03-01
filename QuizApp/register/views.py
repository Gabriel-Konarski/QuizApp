from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect("/")
        else:
            messages.success(request, "There was an error, Try again...")
            return redirect("login")

    else:
        return render(request, 'register/login.html', {})


def logout_user(request):
    logout(request)

    return redirect("login")