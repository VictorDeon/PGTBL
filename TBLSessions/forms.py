from pagedown.widgets import PagedownWidget
from .models import TBLSession
from django import forms


class TBLSessionForm(forms.ModelForm):
    """
    Form to create a new tbl session.
    """

    irat_datetime = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    grat_datetime = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = [
            'title', 'description', 'is_closed',
            'irat_datetime', 'irat_duration',
            'grat_datetime', 'grat_duration',
            'practical_available', 'peer_review_available'
        ]

        # Widgets about some fields
        widgets = {
            'description': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            )
        }
