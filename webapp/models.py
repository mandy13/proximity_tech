from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.username + (" : Student" if self.is_student else " : Instructor")

# class Instructor(models.Model):
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name
#
#
# class Student(models.Model):
#     name = models.CharField(max_length=30)


class Subject(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)


class Tags(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.id) + " " + self.name


class Course(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False)
    viewed = models.IntegerField(default=0)


class Webinar(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subject = models.ManyToManyField(Subject)
    course = models.ManyToManyField(Course)
    webinar = models.FileField(upload_to='webinars/')
    tags = models.ManyToManyField(Tags)
    viewed = models.IntegerField(default=0)


class Video(models.Model):
    title = models.CharField(max_length=100)
    course = models.ManyToManyField(Course)
    subject = models.ManyToManyField(Subject)
    tags = models.ManyToManyField(Tags)
    video = models.FileField(upload_to='videos/')
    viewed = models.IntegerField(default=0)
