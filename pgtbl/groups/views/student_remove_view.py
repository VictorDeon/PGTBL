from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import DeleteView
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group

# Get the custom user from settings
User = get_user_model()


class StudentRemoveView(LoginRequiredMixin,
                        PermissionMixin,
                        DeleteView):
    """
    Remove student from groups.
    """

    template_name = 'groups/students.html'
    permissions_required = ['change_own_group']

    def get_discipline(self):
        """
        Get the specific discipline by url.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_group(self):
        """
        Get the specific group by url
        """

        group = get_object_or_404(
            Group,
            pk=self.kwargs.get('group_id', '')
        )

        return group

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'groups:list',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url

    def delete(self, request, *args, **kwargs):
        """
        Redirect to success url after remove the specific student
        from group.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('student_id', '')
        )

        self.remove_from_group(user)

        return redirect(self.get_success_url())

    def remove_from_group(self, student):
        """
        Remove specific student from group.
        """

        group = self.get_group()

        group.students.remove(student)

        messages.success(
            self.request,
            _("The student {0} is removed from {1}"
              .format(student.get_short_name(), group.title))
        )
