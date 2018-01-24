from .models import iRAT, gRAT, PracticalTest
from django import forms


class iRATForm(forms.ModelForm):
    """
    Form to create a iRAT test.
    """

    datetime = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    class Meta:
        model = iRAT
        fields = ['time', 'datetime', 'is_closed']
