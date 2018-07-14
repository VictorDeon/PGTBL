from django import forms
from pagedown.widgets import PagedownWidget
from TBLSessions.models import TBLSession


class PracticalTestForm(forms.ModelForm):
    """
    Form to update the practical test.
    """

    class Meta:
        model = TBLSession
        fields = [
            'practical_description',
            'practical_available',
            'practical_weight'
        ]

        # Widgets about some fields
        widgets = {
            'practical_description': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            )
        }
