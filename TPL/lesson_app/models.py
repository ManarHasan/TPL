from django.db import models
from TPL_app.models import Teacher
from parent_app.models import Parent, Child
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class Lesson_Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (len(postData['title']) < 2):
            errors['title'] = "title should have at least many characters"
        elif not(NAME_REGEX.match(postData['title'])):
            errors['title'] = "title: Invalid title"

        if (len(postData['description ']) < 5):
            errors['description'] = "description  should have at least many characters"
        return errors


     





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



