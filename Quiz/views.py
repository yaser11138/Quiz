from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm


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
        return render(
            request, "Quiz/Quiz.html", context={"quiz": quiz, "question": question}
        )


def quiz_result(request, quiz_id):
    student = request.user.student
    quiz = Quiz.objects.get(id=quiz_id)
    score = quiz.calculate_score(student)
    return render(
        request, "Quiz/Quiz_result.html", context={"quiz": quiz, "score": score}
    )


def quiz_list(request):
    if request.user.is_student():
        quizzes = Quiz.objects.all()
        return render(request, "Quiz/homepage.html", context={"quizzes": quizzes})
    else:
        quizzes = Quiz.objects.filter(owner=request.user.teacher)
        return render(request, "Quiz/teacher-panel.html", context={"quizzes": quizzes})


def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save(teacher=request.user.teacher)
            return redirect("quiz_list")
        else:
            return render(request, "Quiz/Create.html", context={"form": form})
    else:
        form = QuizForm()
        return render(request, "Quiz/Create.html", context={"form": form})


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


def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.is_owner(teacher=request.user.teacher):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                form.save(quiz=quiz)
                redirect(reverse("quiz_details", args={quiz.id}))
            else:
                return render(request, "Quiz/Create.html", context={"form": form})
        else:
            form = QuestionForm()
            return render(request, "Quiz/Create.html", context={"form": form})
    else:
        return redirect("quiz_list")


def delete_question(request, quiz_id, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect(reverse("quiz_details", args={"quiz_id": quiz_id}))
