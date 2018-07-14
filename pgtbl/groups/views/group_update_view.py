from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.forms import StudentGroupForm
from groups.models import Group


class GroupUpdateView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    View to update a specific group.
    """

    model = Group
    template_name = 'groups/form.html'
    context_object_name = 'group'
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

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside group template.
        """

        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('Group updated successfully.'))

        return super(GroupUpdateView, self).form_valid(form)

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
