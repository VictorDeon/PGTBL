from django import forms
from questions.models import Question, Alternative


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
