from django import forms
from questions.models import Question


class QuestionForm(forms.ModelForm):
    """
    Form to create and update questions.
    """

    class Meta:
        model = Question
        fields = ['title', 'level', 'topic', 'is_exercise']


class AnswerQuestionForm(forms.Form):
    """
    Form to insert scores from each alternative.
    """

    score = forms.IntegerField(
        initial=0,
        max_value=4,
        min_value=0
    )


# Insert a form to each alternative of question (4 forms)
AnswerQuestionFormSet = forms.formset_factory(
    AnswerQuestionForm,
    extra=4
)
