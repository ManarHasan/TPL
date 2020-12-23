from django.db import models
from TPL_app.models import *
from parent_app.models import *


class Lesson_Manager(models.Manager):
    def validator(self, postData):
        return True


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_students = models.IntegerField()
    price = models.IntegerField()
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Lesson_Manager()
