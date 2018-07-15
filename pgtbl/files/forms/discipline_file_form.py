from files.models import DisciplineFile
from django import forms


class DisciplineFileForm(forms.ModelForm):
    """
    Form to create a new file.
    """

    class Meta:
        model = DisciplineFile
        fields = ['title', 'extension', 'description', 'archive']
