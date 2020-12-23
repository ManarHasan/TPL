from django.db import models
from lesson_app.models import Lesson


class Teacher_Manager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if self.validate_text(postData['first_name']) == 0:
            errors["first_name"] = "You must enter a name"
        if self.validate_text(postData['first_name']) == 1:
            errors["fname_length"] = "first name is too short"
        if self.validate_text(postData['last_name']) == 0:
            errors["last_name"] = " you must enter a last name"
        if self.validate_text(postData["last_name"]) == 1:
            errors["lname_length"] = " last name is too short"
        if self.validate_text(postData['occupation']) == 0:
            errors["occupation"] = "You must enter your occupation information"
        if self.validate_text(postData['occupation']) == 1:
            errors["occupation_length"] = "the data you entered is too short"
        if self.validate_text(postData['specialization']) == 0:
            errors["specialization"] = "You must enter your specialization info"
        if self.validate_text(postData['specialization']) == 1:
            errors["specialization_length"] = "the data you entered is too short"


    def email_validator(self, postData):    
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        return errors



class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    lessons = models.ForeignKey(Lesson, related_name="teacher", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Teacher_Manager()

    def validate_text(self, text, min_length=2):
    if text.isalpha == False:
        return 0
    elif len(text) < min_length:
        return 1
    elif len(text) > min_length:
        return 2        