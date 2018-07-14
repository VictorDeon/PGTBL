from django.utils.translation import ugettext_lazy as _
from django import forms
from TBLSessions.models import TBLSession


class GRATForm(forms.ModelForm):
    """
    Form to update gRAT duration and weight.
    """

    class Meta:
        model = TBLSession
        fields = ['grat_duration', 'grat_weight']


class GRATDateForm(forms.ModelForm):
    """
    Form to update datetime of gRAT test.
    """

    grat_datetime = forms.DateTimeField(
        label=_("Date and time to provide the gRAT test"),
        required=False,
        input_formats=['%Y-%m-%dT%H:%M']  # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = ['grat_datetime']


class AnswerGRATQuestionForm(forms.Form):
    """
    Form to insert scores from each alternative.
    """

    SCORES = (
        (4, _('4 Points')),
        (2, _('2 Points')),
        (1, _('1 Point ')),
        (0, _('0 Points'))
    )

    score = forms.ChoiceField(choices=SCORES)
