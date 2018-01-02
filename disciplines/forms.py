from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms

# App imports
from pagedown.widgets import PagedownWidget
from .models import Discipline

# # Get the custom user from settings
User = get_user_model()


class DisciplineForm(forms.ModelForm):
    """
    Form to create a new discipline.
    """

    class Meta:
        model = Discipline
        fields = [
            'title', 'course', 'description', 'classroom',
            'password', 'students_limit', 'monitors_limit'
        ]

        # Widgets about some fields
        widgets = {
            'password': forms.PasswordInput(),
            'description': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            )
        }


class DisciplineEditForm(forms.ModelForm):
    """
    Form to create a new discipline.
    """
    description = forms.CharField(
        widget=PagedownWidget(
            css=("core/css/markdown.css"),
            show_preview=False
        )
    )

    class Meta:
        model = Discipline
        fields = [
            'title', 'course', 'description', 'classroom',
            'password', 'students_limit', 'monitors_limit'
        ]


class EnterDisciplineForm(forms.Form):
    """
    Form to insert students and monitors in the discipline.
    """

    password = forms.CharField(
        label=_('Access Password'),
        max_length=30,
        widget=forms.PasswordInput
    )
