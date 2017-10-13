from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from core.utils import generate_hash_key
from core.email import send_email_template
from .models import PasswordReset

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


class PasswordResetForm(forms.Form):
    """
    Form to reset the user password.
    """

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            _('There is no user found with this email')
        )

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset_password = PasswordReset(user=user, key=key)
        reset_password.save()
        template = 'accounts/reset_password_email.html'
        subject = _('Requesting new password')
        context = {'reset_password': reset_password}
        send_email_template(subject, template, context, [user.email])
