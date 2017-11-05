from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms

# Get the user from settings
User = get_user_model()


class SendEmailForm(forms.Form):
    """
    Form to send email to admin user.
    """

    name = forms.CharField(
        max_length=100,
        label=_("Name"),
        help_text=_("Insert your name.")
    )

    email = forms.EmailField(
        label=_("Email"),
        help_text=_("Insert your email.")
    )

    message = forms.CharField(
        max_length=1000,
        label=_("Message"),
        help_text=_("Insert the message."),
        widget=forms.Textarea
    )
