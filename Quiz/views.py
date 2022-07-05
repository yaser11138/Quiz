from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from .models import Quiz, Question, Answer
from .forms import QuestionForm


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
    quizzes = Quiz.objects.all()
    return render(request,"Quiz/homepage.html",context={"quizzes":quizzes})