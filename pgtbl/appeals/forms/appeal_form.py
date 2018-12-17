from pagedown.widgets import PagedownWidget

from appeals.models import Appeal
from django import forms


class AppealForm(forms.ModelForm):
    """
    Form to create a new appeal to tbl session.
    """

    class Meta:
        model = Appeal
        fields = ['title', 'question', 'description']

        # Widgets about some fields
        widgets = {
            'description': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            )
        }
