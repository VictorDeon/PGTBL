from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from .forms import UserCreationForm

# Get the custom user from settings
User = get_user_model()


class RegisterView(CreateView):
    """
    Class to create a new user.
    """

    model = User
    template_name = 'accounts/register.html'

    # Generate the UserCreationForm
    form_class = UserCreationForm

    # Redirect to login page only when the url is requested
    success_url = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Class to read a profile user.
    """

    template_name = 'accounts/profile.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Edit personal information from user.
    """

    model = User
    template_name = 'accounts/update.html'

    # Generate the forms with this fields
    fields = ['photo', 'name', 'email', 'institution', 'course']

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        """
        Search a ID or slug from url and return a object from model.
        In this case return the current user logged from model.
        """

        return self.request.user


class EditPasswordView(LoginRequiredMixin, FormView):
    """
    Edit password from user.
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

        # Get the get_form_kwargs() from the original class
        # (PasswordChangeForm)
        kwargs = super(EditPasswordView, self).get_form_kwargs()

        # Insert the parameter logged user into the template
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # When the form is valid save the instance
        form.save()

        # Return to form_valid function from django.
        return super(EditPasswordView, self).form_valid(form)
