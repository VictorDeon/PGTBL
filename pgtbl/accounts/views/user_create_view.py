# Django imports
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import CreateView

# Application imoports
from accounts.forms import UserCreationForm

# Get the custom user from settings
User = get_user_model()


class UserCreateView(CreateView):
    """
    Class to create a new user.
    """

    model = User
    template_name = 'accounts/register.html'
    form_class = UserCreationForm

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        """
        Receive the form already validated.
        Logs the user into the system.
        """

        # Get the user saved by form.
        user = form.save()

        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        if user.is_teacher:
            messages.success(
                self.request,
                _("Teacher created successfully.")
            )
        else:
            messages.success(
                self.request,
                _("Student created successfully.")
            )

        return HttpResponseRedirect(self.success_url)
