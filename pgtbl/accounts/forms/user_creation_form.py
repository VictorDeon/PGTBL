from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms

# Get the user from settings
User = get_user_model()


class UserCreationForm(CreationForm):
    """
    Create a form to add a new user that work with django admin.
    """

    CHOICES = (
        (True, _('Teacher')),
        (False, _('Student'))
    )

    is_teacher = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        # password and password confirmation has in the UserCrationForm
        fields = [
            'name',
            'username',
            'email',
            'is_teacher'
        ]
