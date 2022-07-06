from .models import Teacher, Student
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(UserCreationForm):
    TypeChoice = (
        ("T", "Teacher"),
        ("S", "Student"),
    )
    type = forms.ChoiceField(choices=TypeChoice)
    teacher_id = forms.IntegerField(required=False)
    grade = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email == "":
            raise forms.ValidationError("This field is required")
        elif User.objects.filter(email=email):
            raise forms.ValidationError("this field is already used")
        else:
            return email

    def clean_grade(self):
        grade = self.cleaned_data["grade"]
        if self.cleaned_data["type"] == "S":
            if grade is None:
                raise forms.ValidationError("This field is required")
            elif grade >= 12:
                raise forms.ValidationError("Grade must be between 1 and 12")
            else:
                return grade
        else:
            return None

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data["teacher_id"]
        if self.cleaned_data["type"] == "T":
            if teacher_id is None:
                raise forms.ValidationError("This  is Required")
            else:
                return teacher_id
        else:
            return None

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data["type"] == "T":
                Teacher.objects.create(user=user, teacher_id=self.cleaned_data["teacher_id"])
            elif self.cleaned_data["type"] == "S":
                Student.objects.create(user=user, grade=self.cleaned_data["grade"])
        return user
