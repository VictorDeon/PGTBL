from django.contrib.auth import get_user_model
from django import forms

# Get the user from settings
User = get_user_model()


class UserForm(forms.ModelForm):
    """
    Create a form that work with django admin.
    """

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
            'is_teacher',
            'is_active',
            'is_staff'
        ]
