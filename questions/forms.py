from .models import Question
from django import forms


class QuestionForm(forms.ModelForm):
    """
    Form to create and update questions.
    """

    class Meta:
        model = Question
        fields = ['title', 'level', 'topic', 'is_exercise']
