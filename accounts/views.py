from django.views.generic import CreateView
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
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    # After create user go to login page.
    # reverse_lazy get the url only when the url is requested
    success_url = reverse_lazy('accounts:login')
