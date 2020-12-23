from django.shortcuts import render


def index(request):
    return render(request, "signup_login.html")


def parent_profile(request):
    return render(request, "parent_profile.html")


def teacher_profile(request):
    return render(request, "teacher_profile.html")


def details(request):
    return render(request, "schedule_day.html")


def home(request):
    return render(request, "home_page.html")
