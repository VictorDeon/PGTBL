from django import forms
from .models import Group


class StudentGroupForm(forms.ModelForm):
    """
    Form to create a new group.
    """

    class Meta:
        model = Group
        fields = ['title', 'students_limit']
