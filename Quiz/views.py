from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm
from .authentication import is_teacher


@login_required(login_url=reverse_lazy("login"))
def take_quiz(request, quiz_id, question_id=None):
    student = request.user.student
    quiz = Quiz.objects.get(id=quiz_id)

    if student not in quiz.particpations.all():
        quiz.particpations.add(request.user.student)

    if request.method == "POST":
        question = Question.objects.get(id=question_id)
        choice = request.POST.get("choice", " ")
        Answer.objects.create(user_answer=choice, student=student, question=question)
        return redirect(reverse("quiz_start", args=(quiz_id,)))
    else:
        if quiz.is_finished(student=student):
            return redirect(reverse("quiz_result", args=(quiz_id,)))
        question = quiz.qet_qeustion(student=request.user.student)
        return render(request, "Quiz/Quiz.html", context={"quiz": quiz, "question": question})


@login_required(login_url=reverse_lazy("login"))
def quiz_result(request, quiz_id):
    student = request.user.student
    quiz = Quiz.objects.get(id=quiz_id)
    score = quiz.calculate_score(student)
    return render(request, "Quiz/Quiz_result.html", context={"quiz": quiz, "score": score})


def quiz_homepage(request):
    if request.user.is_authenticated and request.user.is_teacher():
        return redirect("teacher-panel")
    quizzes = Quiz.objects.annotate(Count("questions")).filter(questions__count__gt=0)
    return render(request, "Quiz/homepage.html", context={"quizzes": quizzes})


@user_passes_test(is_teacher, login_url=reverse_lazy("login"))
def quiz_teacherpanel(request):
    quizzes = Quiz.objects.filter(owner=request.user.teacher)
    return render(request, "Quiz/teacher-panel.html", context={"quizzes": quizzes})


@user_passes_test(is_teacher, login_url=reverse_lazy("quiz-home"))
def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save(teacher=request.user.teacher)
            return redirect(reverse("teacher-panel"))
        else:
            return render(request, "Quiz/Create.html", context={"form": form})
    else:
        form = QuizForm()
        return render(request, "Quiz/Create.html", context={"form": form})


@user_passes_test(is_teacher, login_url=reverse_lazy("quiz-home"))
def quiz_details(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == "POST":
        form = QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save(teacher=request.user.teacher)
        return render(request, "Quiz/Quiz_details.html", context={"quiz": quiz, "form": form})
    else:
        form = QuizForm(instance=quiz)
        return render(request, "Quiz/Quiz_details.html", context={"quiz": quiz, "form": form})


@user_passes_test(is_teacher, login_url=reverse_lazy("quiz-home"))
def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.is_owner(teacher=request.user.teacher):

        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                form.save(quiz=quiz)
                return redirect(reverse("quiz_details", args={quiz.id}))
            else:
                return render(request, "Quiz/Create.html", context={"form": form})
        else:
            form = QuestionForm()
            return render(request, "Quiz/Create.html", context={"form": form})

    else:
        return redirect("teacher-panel")


@user_passes_test(is_teacher, login_url=reverse_lazy("quiz-home"))
def delete_question(request, quiz_id, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect(reverse("quiz_details", args={"quiz_id": quiz_id}))
