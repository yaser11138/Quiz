from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def is_student(self):
        return hasattr(self, "student")

    def is_teacher(self):
        return hasattr(self, "teacher")


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.IntegerField()
