# Django app
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth import get_user_model
from django import forms

# Get the user from settings
User = get_user_model()


class UserCreationForm(CreationForm):
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


class PasswordResetForm(forms.Form):
    """
    Form to reset the user password.
    """

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        """
        Verify if the email exists in the system and return it.
        """

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            _('There is no user found with this email')
        )
