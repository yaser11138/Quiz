from django import template

register = template.Library()


@register.filter(name='is_finished')
def is_finished(quiz, student=None):
    if student is None:
        return False
    return quiz.is_finished(student)
