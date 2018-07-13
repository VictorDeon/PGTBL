from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import UpdateView

# Get the custom user from settings
User = get_user_model()


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Edit personal information from user.
    """

    model = User
    template_name = 'accounts/edit_information.html'

    # Generate the forms with this fields
    fields = ['photo', 'name', 'username', 'email', 'institution', 'course']

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        """
        Search a ID or slug from url and return a object from model.
        In this case return the current user logged from model.
        """

        return self.request.user

    def form_valid(self, form):
        """
        Get the form validated, send successfully message and return the
        success_url.
        """

        messages.success(
            self.request,
            _("User updated successfully.")
        )

        # Redirect to success_url
        return super(EditProfileView, self).form_valid(form)
