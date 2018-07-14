from files.models import SessionFile
from django import forms


class SessionFileForm(forms.ModelForm):
    """
    Form to create a new file to tbl session.
    """

    class Meta:
        model = SessionFile
        fields = ['title', 'extension', 'description', 'archive']
