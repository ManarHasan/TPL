from django.db import models
from TPL_app.models import Teacher
import re


class Parent_Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        if self.validate_text(postData['fname']) == 1:
            errors["fname"] = "This name is too short!"
        if self.validate_text(postData['fname']) == 0:
            errors["fname_letters"] = "A name must be Abc characters only! Sorry Elon Musk!"
        if self.validate_text(postData['lname']) == 1:
            errors["lname"] = "This name is too short!"
        if self.validate_text(postData['lname']) == 0:
            errors["lname_letters"] = "A name must be Abc characters only!"
        if self.validate_email(postData['email']) == 0:
            errors["email"] = "Invalid email"
        if self.validate_email(postData['email']) == 1:
            errors["email_exists"] = "This email already exists"
        if self.validate_text(postData['password'], max_length=8) == 1:
            errors["password"] = "Password is too short!"
        if self.validate_text(postData['occupation'], max_length=5) == 1:
            errors["occupation"] = "Occupation must be at least 5 charcters"
        return errors


class Parent(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Parent_Manager()

    def validate_text(self, text, min_length=2):
        if text.isalpha == False:
            return 0
        elif len(text) < min_length:
            return 1
        elif len(text) > min_length:
            return 2

    def validate_email(self, email):
        regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        if re.search(regex, email):
            if not self.is_duplicate_email(email):
                return 2
            return 1
        return 0

    def is_duplicate_email(self, email):
        parent = Parent.objects.filter(email=email).values()
        if len(parent):
            return True
        return False


class Child_Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        if self.validate_text(postData['fname']) == 1:
            errors["fname"] = "This name is too short!"
        if self.validate_text(postData['fname']) == 0:
            errors["fname_letters"] = "A name must be Abc characters only! Sorry Elon Musk!"
        return errors


class Child(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    grade = models.IntegerField()
    gender = models.CharField(max_length=6)
    parent = models.ForeignKey(
        Parent, related_name="children", on_delete=models.CASCADE)
    lessons = models.ManyToManyField(
        Teacher, through="Lesson")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Child_Manager()

    def lastName(self, postData):
        self.last_name = postData['lname']
