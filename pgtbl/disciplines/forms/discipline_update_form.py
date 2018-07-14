from django import forms
from pagedown.widgets import PagedownWidget
from disciplines.models import Discipline


class DisciplineUpdateForm(forms.ModelForm):
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
