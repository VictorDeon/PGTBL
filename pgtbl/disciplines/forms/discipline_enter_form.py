from django.utils.translation import ugettext_lazy as _
from django import forms


class DisciplineEnterForm(forms.Form):
    """
    Form to insert students and monitors in the discipline.
    """

    password = forms.CharField(
        label=_('Access Password'),
        max_length=30,
        widget=forms.PasswordInput
    )
