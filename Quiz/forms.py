from django import forms
from .models import Quiz, Question


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ("name", "subject")

    def save(self, commit=True, teacher=None):
        quiz = super().save(commit=False)
        quiz.owner = teacher
        if commit:
            quiz.save()
        return quiz


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("title", "option1", "option2", "option3", "option4", "answer", "score")

    def save(self, commit=True, quiz=None):
        question = super().save(commit=False)
        question.quiz = quiz
        if commit:
            question.save()
        return question