from django.utils.translation import ugettext_lazy as _
from django import forms
from TBLSessions.models import TBLSession


class IRATForm(forms.ModelForm):
    """
    Form to update iRAT duration and weight.
    """

    class Meta:
        model = TBLSession
        fields = ['irat_duration', 'irat_weight']


class IRATDateForm(forms.ModelForm):
    """
    Form to update datetime of iRAT test.
    """

    irat_datetime = forms.DateTimeField(
        label=_("Date and time to provide the iRAT test"),
        required=False,
        input_formats=['%Y-%m-%dT%H:%M']  # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = ['irat_datetime']
