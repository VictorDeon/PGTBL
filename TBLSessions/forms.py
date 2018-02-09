from django.utils.translation import ugettext_lazy as _
from django import forms
from pagedown.widgets import PagedownWidget
from .models import TBLSession


class TBLSessionForm(forms.ModelForm):
    """
    Form to create a new tbl session.
    """

    irat_datetime = forms.DateTimeField(
        label=_("Date and time to provide the iRAT test"),
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    grat_datetime = forms.DateTimeField(
        label=_("Date and time to provide the gRAT test"),
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = [
            'title', 'description', 'is_closed',
            'irat_datetime', 'irat_duration', 'irat_weight',
            'grat_datetime', 'grat_duration', 'grat_weight',
            'practical_available', 'practical_weight',
            'peer_review_available', 'peer_review_weight'
        ]

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
        fields = ['practical_description']

        # Widgets about some fields
        widgets = {
            'practical_description': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            )
        }
