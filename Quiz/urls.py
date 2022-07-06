from django.urls import path
from Quiz import views

urlpatterns = [
    path("<int:quiz_id>/<int:question_id>", views.take_quiz, name='quiz_run'),
    path("<int:quiz_id>/", views.take_quiz, name="quiz_start"),
    path("<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
    path("list/", views.quiz_list, name="quiz_list"),
    path("add/", views.add_quiz, name="add_quiz"),
    path("<int:quiz_id>/details/", views.quiz_details, name="quiz_details"),
    path("<int:quiz_id>/question/add/", views.add_question, name="question_add"),
    path("<int:quiz_id>/question/<int:question_id>/delete", views.delete_question, name="delete_question"),
]
