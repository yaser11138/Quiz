from django.db import models
from Accounts.models import Student, Teacher


class Quiz(models.Model):
    name = models.CharField(max_length=10)
    subject = models.CharField(max_length=10)
    particpations = models.ManyToManyField(Student, blank=True)
    owner = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    @property
    def score(self):
        return Question.objects.filter(quiz=self).aggregate(score=models.Sum("score"))["score"]

    def calculate_score(self, student):
        score = 0
        for question in self.questions.all():
            if question.answers.get(student=student).is_correct:
                score += question.score
        return score

    def is_finished(self, student):
        if len(Question.objects.filter(quiz=self).exclude(answers__student=student)) == 0:
            return True
        else:
            return False

    def qet_qeustion(self, student):
        return Question.objects.filter(quiz=self).exclude(answers__student=student).order_by("?")[0]

    def is_owner(self, teacher):
        if self.owner == teacher:
            return True
        else:
            return False


class Question(models.Model):
    title = models.CharField(max_length=256)
    option1 = models.CharField(max_length=256)
    option2 = models.CharField(max_length=256)
    option3 = models.CharField(max_length=256)
    option4 = models.CharField(max_length=256)
    answer = models.CharField(max_length=256)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, related_name="questions")
    score = models.IntegerField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user_answer = models.CharField(max_length=256)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="students")

    @property
    def is_correct(self):
        if self.user_answer == self.question.answer:
            return True
        else:
            return False
