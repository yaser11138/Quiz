from django import forms


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields["choice"] = forms.ChoiceField(
            choices=((question.option1, question.option1),
                     (question.option2, question.option2),
                     (question.option3, question.option3),
                     question.option4, question.option4))
        self.fields["title"] = question.title

