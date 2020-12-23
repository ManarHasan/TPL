from django.db import models
from lesson_app.models import *
from TPL_app.models import *


class Parent_Manager(models.Manager):
    def validator(self, postData):
        return True


class Parent(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Parent_Manager()


class Child_Manager(models.Manager):
    def validator(self, postData):
        return True


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
