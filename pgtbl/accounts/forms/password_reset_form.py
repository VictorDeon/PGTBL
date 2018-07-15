from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms

# Get the user from settings
User = get_user_model()


class PasswordResetForm(forms.Form):
    """
    Form to reset the user password.
    """

    email = forms.EmailField(label='E-mail', required=True)

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
