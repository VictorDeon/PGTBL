from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from groups.forms import StudentGroupForm


class GroupCreateView(LoginRequiredMixin,
                      PermissionMixin,
                      CreateView):
    """
    View to create a new group to discipline.
    """

    model = Group
    template_name = 'groups/list.html'
    form_class = StudentGroupForm

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

    def form_valid(self, form):
        """
        Receive the form already validated to create a group.
        """

        form.instance.discipline = self.get_discipline()

        form.save()

        messages.success(self.request, _('Group created successfully.'))

        return super(GroupCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to group list with error.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url
