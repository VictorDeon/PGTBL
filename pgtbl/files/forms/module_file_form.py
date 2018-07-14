from files.models import ModuleFile
from django import forms


class ModuleFileForm(forms.ModelForm):
    """
    Form to create a new file to tbl session.
    """

    class Meta:
        model = ModuleFile
        fields = ['title', 'extension', 'description', 'archive']
