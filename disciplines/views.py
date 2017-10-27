"""
The list of user disciplines is in accounts.views.ProfileView
Disciplines functionalities
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, UpdateView, DeleteView
)
from core.mixins import PermissionRequiredMixin
from .forms import DisciplineForm
from .models import Discipline

# # Get the custom user from settings
User = get_user_model()


class DisciplineCreationView(LoginRequiredMixin,
                             PermissionRequiredMixin,
                             CreateView):
    """
    View to create a new discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    form_class = DisciplineForm
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    user_check_failure_path = reverse_lazy('accounts:profile')
    permission_required = 'disciplines.add_discipline'

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # Specifies who is the creator of the discipline
        form.instance.teacher = self.request.user

        # Return to form_valid function from django to finish creation.
        return super(DisciplineCreationView, self).form_valid(form)


class DisciplineUpdateView(LoginRequiredMixin,
                           PermissionRequiredMixin,
                           UpdateView):
    """
    View to update a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    fields = [
        'title', 'course', 'description', 'classroom',
        'password', 'student_limit'
    ]
    success_url = reverse_lazy('accounts:profile')
    slug_url_kwargs = 'slug'

    user_check_failure_path = reverse_lazy('accounts:profile')
    permission_required = 'disciplines.change_discipline'


class DisciplineDeleteView(LoginRequiredMixin,
                           PermissionRequiredMixin,
                           DeleteView):
    """
    View to delete a specific discipline.
    """

    model = Discipline
    success_url = reverse_lazy('accounts:profile')
    slug_url_kwargs = 'slug'

    user_check_failure_path = reverse_lazy('accounts:profile')
    permission_required = 'disciplines.change_discipline'
