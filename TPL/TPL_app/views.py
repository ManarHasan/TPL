from django.shortcuts import render, redirect
from .models import Parent, Child, Lesson, Teacher
from django.forms.models import model_to_dict
from . import models
import datetime
from django.contrib import messages
import bcrypt


def login_registration(request):
    return render(request, "signup_login.html")


def register(request):
    if request.POST['option'] == "parent":
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        errors = models.parent_validator(
            request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        user = models.add_parent(request.POST, pw_hash)
        child = models.add_child(request.POST, user.id)
        if 'user_id' not in request.session:
            request.session['type'] = "parent"
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('/parent-profile/'+str(request.session['user_id']))
    if request.POST['option'] == "teacher":
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        errors = models.parent_validator(
            request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        user = models.add_teacher(request.POST, pw_hash)
        if 'user_id' not in request.session:
            request.session['type'] = "teacher"
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('/teacher-profile/'+str(request.session['user_id']))


def login(request):
    if request.POST['options'] == "parent":
        email = request.POST['email']
        user = models.get_parent(email)
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            if user is not None:
                if 'user_id' not in request.session:
                    request.session['type'] = "parent"
                    request.session['user_id'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                return redirect('/parent-profile/'+str(request.session['user_id']))
    if request.POST['options'] == "teacher":
        email = request.POST['email']
        user = models.get_teacher(email)
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            if user is not None:
                if 'user_id' not in request.session:
                    request.session['type'] = "teacher"
                    request.session['user_id'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                return redirect('/teacher-profile/'+str(request.session['user_id']))
    return redirect('/')


def logout(request):
    del request.session['user_id']
    del request.session['first_name']
    del request.session['last_name']
    del request.session['type']
    return redirect('/')


def parent_profile(request, id):
    # if ['user_id'] not in request.session:
    #     messages.error(request, "You must be logged in to view this page")
    parent = Parent.objects.get(id=id)
    children = parent.children.all()
    all_lessons = []
    for child in children:
        all_lessons.append(Lesson.objects.filter(child=child.id))

    context = {
        "parent": parent,
        "children": children,
        "all_lessons": all_lessons
    }
    return render(request, "parent_profile.html", context)


def teacher_profile(request, id):
    teacher = Teacher.objects.get(id=id)
    students = teacher.lessons.all()
    all_lessons_for_each_student = []
    all_teacher_lessons = Lesson.objects.filter(teacher=Teacher.objects.get(id=id))
    all_times = []
    for child in students:
        all_lessons_for_each_student.append(Lesson.objects.filter(
            teacher=teacher, child=child.id))
    for child in all_lessons_for_each_student:
        for lessons in child:
            print(lessons.day)
            
    context = {
        "teacher": teacher,
        "students": students,
        "all_teacher_lessons": all_teacher_lessons,
        "all_lessons": all_lessons_for_each_student,
    }
    if request.session['type'] == "parent":
        parent = Parent.objects.get(id=request.session['user_id'])
        children = parent.children.all()
        context['children'] = children
    return render(request, "teacher_profile.html", context)


def add_lesson(request, id):
    teacher = Teacher.objects.get(id=id)
    errors = models.lesson_validator(
        request.POST, id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/teacher-profile/'+str(id))
    lesson = models.add_lesson(request.POST, id)
    return redirect('/teacher-profile/'+str(id))


def add_child_form(request, d, n, tid):
    parent = Parent.objects.get(id=request.session['user_id'])
    children = parent.children.all()
    context={
        'children': children,
        "d":d,
        "n": n,
        "tid": tid
        }
    return render(request, "schedule_day.html",context)

def signup_to_lesson(request, id, d, n, tid):
    child = Child.objects.get(id=request.POST['child'])
    teacher = Teacher.objects.get(id=tid)
    lesson = Lesson.objects.get(teacher=teacher, day=d, time=n)
    lesson.child = child
    lesson.save()
    return redirect('/teacher-profile/'+str(tid))

def home(request):
    return render(request, "home_page.html")
