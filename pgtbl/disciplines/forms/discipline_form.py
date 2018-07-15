from django import forms
from pagedown.widgets import PagedownWidget
from disciplines.models import Discipline


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
