from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import FormView

# Application imoports
from accounts.models import PasswordReset


class ResetPasswordConfirmView(FormView):
    """
    Insert new password from email link.
    """

    template_name = 'accounts/reset_password_confirm.html'

    # Use SetPasswordForm from django
    form_class = SetPasswordForm

    # Redirect to login page.
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        """
        Insert arguments inside form.
        """

        # Get all arguments kwargs from SetPasswordForm
        kwargs = super(ResetPasswordConfirmView, self).get_form_kwargs()

        # Get the user with kwargs key to reset his password
        reset = get_object_or_404(
            PasswordReset,
            key=self.kwargs.get('key')
        )

        # Change user and data from form
        kwargs['user'] = reset.user
        kwargs['data'] = self.request.POST or None

        return kwargs

    def form_valid(self, form):
        """
        Validated form and reset password.
        """

        # In this case when you insert new kwargs, you need to save
        # the instance again
        form.save()

        messages.success(
            self.request,
            _("Your password was successfully updated.")
        )

        # Redirect to success_url
        return super(ResetPasswordConfirmView, self).form_valid(form)
