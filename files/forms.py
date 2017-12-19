from django import forms
from .models import File


class FileForm(forms.ModelForm):
    """
    Form to create a new file.
    """

    class Meta:
        model = File
        fields = ['title', 'extension', 'description', 'archive']
