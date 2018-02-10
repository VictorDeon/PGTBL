from django.utils.translation import ugettext_lazy as _
from django import forms
from pagedown.widgets import PagedownWidget
from .models import TBLSession


class TBLSessionForm(forms.ModelForm):
    """
    Form to create a new tbl session.
    """

    class Meta:
        model = TBLSession
        fields = ['title', 'description', 'is_closed']

        # Widgets about some fields
        widgets = {
            'description': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            )
        }

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
