from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

# Get the user from settings
User = get_user_model()


class UserCreationForm(UserCreationForm):
    """
    Create a form to add a new user that work with django admin.
    """

    CHOICES = ((True, _('Teacher')), (False, _('Student')))
    is_teacher = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        # password and password confirmation has in the UserCrationForm
        fields = [
            'username',
            'email',
            'is_teacher',
        ]


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
