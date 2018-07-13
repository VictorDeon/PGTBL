from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView


class PasswordUpdateView(LoginRequiredMixin, FormView):
    """
    Edit user password.
    """

    template_name = 'accounts/edit_password.html'

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')

    # Generate the PasswordChangeForm from django
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        """
        Generates the arguments that will be passed to the form.
        """

        # Get the kwargs from the original class FormView
        kwargs = super(PasswordUpdateView, self).get_form_kwargs()

        # Insert the parameter logged user into the form template
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # In this case when you insert new kwargs, you need to save
        # the instance again
        form.save()

        messages.success(self.request, _("Password updated successfully."))

        # Redirect to success_url
        return super(PasswordUpdateView, self).form_valid(form)
