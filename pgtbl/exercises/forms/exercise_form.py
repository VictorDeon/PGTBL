from django import forms
from modules.models import TBLSession


class ExerciseForm(forms.ModelForm):
    """
    Form to update exercise gamification weight.
    """

    class Meta:
        model = TBLSession
        fields = ['exercise_score']