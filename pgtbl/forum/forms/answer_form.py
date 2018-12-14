from django import forms

from forum.models import Answer


class AnswerForm(forms.ModelForm):
    """
    Form to crud a answer.
    """

    class Meta:
        model = Answer
        fields = ['content']