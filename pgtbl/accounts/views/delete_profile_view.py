from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import DeleteView

# Get the custom user from settings
User = get_user_model()


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    """
    Delete the user account
    """

    model = User

    # Redirect to home page
    success_url = reverse_lazy('core:home')

    def get_object(self):
        """
        Search a ID or slug from url and return a object from model.
        In this case return the current user logged from model.
        """

        return self.request.user

    def get_success_url(self):
        """
        Redirect to success_url and show a message.
        """

        messages.success(self.request, _("Accounts deleted successfully."))

        # Redirect to success_url
        return super(DeleteProfileView, self).get_success_url()
