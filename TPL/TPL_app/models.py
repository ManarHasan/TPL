from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Parent(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Child(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    grade = models.IntegerField()
    gender = models.CharField(max_length=6)
    parent = models.ForeignKey(
        Parent, related_name="children", on_delete=models.CASCADE)
    lessons = models.ManyToManyField(
        Teacher, through="Lesson", related_name="lessons")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_students = models.IntegerField()
    price = models.IntegerField()
    style = models.CharField(max_length=255, null=True)
    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def add_parent(postData, pw_hash):
    user = Parent.objects.create(
        first_name=postData['fname'], last_name=postData['lname'], occupation=postData['occupation'], email=postData['email'], password=pw_hash)
    return user


def add_child(postData, user_id):
    child = Child.objects.create(first_name=postData['child_name'], last_name=postData['lname'],
                                 age=postData['age'], gender=postData['gender'], grade=postData['grade'], parent=Parent.objects.get(id=user_id))
    return child


def add_teacher(postData, pw_hash):
    user = Teacher.objects.create(
        first_name=postData['fname'], last_name=postData['lname'], occupation=postData['occupation'], email=postData['email'], password=pw_hash, specialization=postData['specialization'], education=postData['education'])
    return user


def add_lesson(postData, id):
    time = "2020, "+str(postData['time'])+", " + \
        str(postData['day'])+", " + \
        str(postData['month'])+", 0, 0, tzinfo=<UTC>"
    lesson = Lesson.objects.create(title=postData['title'], description=postData['description'], max_students=1,
                                   price=postData['price'], style=postData['style'], time=time, teacher=Teacher.objects.get(id=id))
    return lesson


def get_parent(email):
    user = Parent.objects.filter(email=email)
    return user[0]


def get_teacher(email):
    user = Teacher.objects.filter(email=email)
    return user[0]


def is_duplicate_email(email):
    parent = Parent.objects.filter(email=email).values()
    if len(parent):
        return True
    return False


def validate_text(text, min_length=2):
    if text.isalpha == False:
        return 0
    elif len(text) < min_length:
        return 1
    elif len(text) > min_length:
        return 2


def validate_email(email):
    regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
    if re.search(regex, email):
        if not is_duplicate_email(email):
            return 2
        return 1
    return 0


def teacher_validator(postData):
    errors = {}
    if validate_text(postData['fname']) == 0:
        errors["first_name"] = "You must enter a name"
    if validate_text(postData['fname']) == 1:
        errors["fname_length"] = "first name is too short"
    if validate_text(postData['lname']) == 0:
        errors["last_name"] = "You must enter a last name"
    # if validate_text(postData["lname"]) == 1:
    #     errors["lname_length"] = "last name is too short"
    if validate_text(postData['occupation']) == 0:
        errors["occupation"] = "You must enter your occupation information"
    if validate_text(postData['occupation']) == 1:
        errors["occupation_length"] = "the data you entered is too short"
    if validate_text(postData['specialization']) == 0:
        errors["specialization"] = "You must enter your specialization info"
    if validate_text(postData['specialization']) == 1:
        errors["specialization_length"] = "the data you entered is too short"
    return errors


def parent_validator(postData):
    errors = {}
    if validate_text(postData['fname']) == 1:
        errors["fname"] = "This name is too short!"
    if validate_text(postData['fname']) == 0:
        errors["fname_letters"] = "A name must be Abc characters only! Sorry Elon Musk!"
    if validate_text(postData['lname']) == 1:
        errors["lname"] = "This name is too short!"
    if validate_text(postData['lname']) == 0:
        errors["lname_letters"] = "A name must be Abc characters only!"
    if validate_email(postData['email']) == 0:
        errors["email"] = "Invalid email"
    if validate_email(postData['email']) == 1:
        errors["email_exists"] = "This email already exists"
    if validate_text(postData['password'], min_length=8) == 1:
        errors["password"] = "Password is too short!"
    if validate_text(postData['occupation'], min_length=5) == 1:
        errors["occupation"] = "Occupation must be at least 5 charcters"
    return errors


def child_validator(postData):
    errors = {}
    if validate_text(postData['fname']) == 1:
        errors["fname"] = "This name is too short!"
    if validate_text(postData['fname']) == 0:
        errors["fname_letters"] = "A name must be Abc characters only! Sorry Elon Musk!"
    return errors


def lesson_validator(postData):
    errors = {}
    if len(postData['title']) < 2:
        errors['title'] = "title should have at least many characters"
    if len(postData['description ']) < 5:
        errors['description'] = "description  should have at least many characters"
    return errors
