from django.contrib import admin
from .models import Teacher,Student,User
# Register your models here.
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass
