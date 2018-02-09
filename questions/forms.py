from django.utils.translation import ugettext_lazy as _
from django import forms
from TBLSessions.models import TBLSession
from .models import Question, Alternative


class QuestionForm(forms.ModelForm):
    """
    Form to create and update questions.
    """

    class Meta:
        model = Question
        fields = ['title', 'level', 'topic', 'is_exercise']


class AlternativeForm(forms.ModelForm):
    """
    Form to create an alternative with inline formset.
    """

    class Meta:
        model = Alternative
        fields = ['title', 'is_correct']


# Djanho allows edit a collection of form in the same page.
# extra: controls the number of forms that will apper
AlternativeFormSet = forms.inlineformset_factory(
    Question,
    Alternative,
    form=AlternativeForm,
    extra=4,
    max_num=4
)


class AnswerQuestionForm(forms.Form):
    """
    Form to insert scores from each alternative.
    """

    score = forms.IntegerField(
        initial=0,
        max_value=4,
        min_value=0
    )

# # Insert a form to each alternative of question (4 forms)
AnswerQuestionFormSet = forms.formset_factory(
    AnswerQuestionForm,
    extra=4
)


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
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = ['irat_datetime']

# gRAT
class AnswerGRATQuestionForm(forms.Form):
    """
    Form to insert scores from each alternative.
    """

    SCORES = (
        (4, _('Option 01')),
        (2, _('Option 02')),
        (1, _('Option 03 ')),
        (0, _('Option 04'))
    )

    score = forms.ChoiceField(choices=SCORES)


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
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = ['grat_datetime']
