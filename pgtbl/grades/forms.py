from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):
    """
    Form to update the students grade.
    """

    class Meta:
        model = Grade
        fields = ['irat', 'grat', 'practical', 'peer_review']
