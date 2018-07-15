from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from groups.forms import StudentGroupForm


class GroupListView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to see all groups of discipline.
    """

    template_name = 'groups/list.html'
    paginate_by = 5
    context_object_name = 'groups'

    # Permissions
    permissions_required = [
        'show_discipline_groups_permission'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(GroupListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = StudentGroupForm()
        return context

    def get_queryset(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups
