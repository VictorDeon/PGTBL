from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth import get_user_model
from django import forms
from core.utils import generate_hash_key
from core.email import send_email_template
from .models import PasswordReset

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

    def save(self):
        """
        Save the password reset object and send a email to user.
        """

        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset_password = PasswordReset(user=user, key=key)
        reset_password.save()
        # Send email
        send_email_template(
            subject=_('Requesting new password'),
            template='accounts/reset_password_email.html',
            context={'reset_password': reset_password},
            recipient_list=[user.email],
        )
