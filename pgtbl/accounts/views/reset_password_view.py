from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import FormView

# Application imoports
from core.email import send_email_template
from core.utils import generate_hash_key
from accounts.forms import PasswordResetForm
from accounts.models import PasswordReset

# Get the custom user from settings
User = get_user_model()


class ResetPasswordView(FormView):
    """
    Reset the user password and send email.
    """

    template_name = 'accounts/reset_password.html'

    # Use the PasswordResetForm
    form_class = PasswordResetForm

    # Redirect to home page
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        """
        Validated form and send email.
        """

        user = User.objects.get(email=form.cleaned_data['email'])

        # Generate unique key to reset password
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

        messages.success(
            self.request,
            _("An email was sent with more details on how to create a new password")
        )

        # Redirect to success_url
        return super(ResetPasswordView, self).form_valid(form)
