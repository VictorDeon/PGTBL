from .models import Question, Alternative
from django import forms


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
        fields = ['alternative_title', 'is_correct']


# Djanho allows edit a collection of form in the same page.
# extra: controls the number of forms that will apper
AlternativeFormSet = forms.inlineformset_factory(
    Question,
    Alternative,
    form=AlternativeForm,
    extra=4,
    max_num=4
)


class AnswerQuestionForm(forms.ModelForm):
    """
    Form to insert scores from each alternative.
    """

    class Meta:
        model = Alternative
        fields = ['score']


# Insert a form to each alternative of question (4 forms)
AnswerQuestionFormSet = forms.formset_factory(
    AnswerQuestionForm,
    extra=4
)
