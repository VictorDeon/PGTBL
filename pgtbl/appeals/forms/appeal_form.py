from appeals.models import Appeal
from django import forms


class AppealForm(forms.ModelForm):
    """
    Form to create a new appeal to tbl session.
    """

    class Meta:
        model = Appeal
        fields = ['title', 'question', 'description']
