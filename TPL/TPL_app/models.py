from django.db import models
from lesson_app.models import *
from parent_app.models import *


class Teacher_Manager(models.Manager):
    def validator(self, postData):
        return True


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    lessons = models.ForeignKey(
        Lesson, related_name="teacher", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Teacher_Manager()
