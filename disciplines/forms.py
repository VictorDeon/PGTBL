from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django import forms
from .models import Discipline

# # Get the custom user from settings
User = get_user_model()


class DisciplineForm(forms.ModelForm):
    """
    Form to create a new discipline.
    """

    class Meta:
        model = Discipline
        fields = [
            'title', 'course', 'description', 'classroom',
            'password', 'student_limit'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self):
        """
        Autocomplete the slug with title before save
        """

        # Get the instance before save (commit=False)
        instance = super(DisciplineForm, self).save(commit=False)
        # Autocomplete slug with title
        instance.slug = slugify(instance.title)
        # Save the instance with slug autocomplete
        instance.save()

        return instance
