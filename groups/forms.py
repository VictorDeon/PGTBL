from django.contrib.auth import get_user_model
from django import forms
from .models import Group

# # Get the custom user from settings
User = get_user_model()


class StudentGroupForm(forms.ModelForm):
    """
    Form to create a new group.
    """

    class Meta:
        model = Group
        fields = ['title', 'students_limit']
