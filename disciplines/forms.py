from django.contrib.auth import get_user_model
from django import forms
from .models import Discipline

# # Get the custom user from settings
User = get_user_model()


class DisciplineCreateForm(forms.ModelForm):
    """
    Form to create a new discipline.
    """

    class Meta:
        model = Discipline
        fields = [
            'title', 'course', 'description', 'classroom',
            'password', 'student_limit'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }
