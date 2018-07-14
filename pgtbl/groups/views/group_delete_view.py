from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group


class GroupDeleteView(LoginRequiredMixin,
                      PermissionMixin,
                      DeleteView):
    """
    View to delete a specific group.
    """

    model = Group

    # Permissions
    permissions_required = [
        'change_own_group'
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

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        messages.success(self.request, _("Group deleted successfully."))

        return success_url
