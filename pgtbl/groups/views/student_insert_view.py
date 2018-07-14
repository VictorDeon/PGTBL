from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from core.generics import ObjectRedirectView
from groups.models import Group

# Get the custom user from settings
User = get_user_model()


class StudentInsertView(LoginRequiredMixin,
                        PermissionMixin,
                        ObjectRedirectView):
    """
    Insert a student inside group.
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

    def action(self, request, *args, **kwargs):
        """
        Insert a student into the group action.
        and redirect to success url
        """

        student = get_object_or_404(
            User,
            pk=self.kwargs.get('student_id', '')
        )

        self.insert(student)

        return redirect(self.get_success_url())

    def insert(self, student):
        """
        Insert student into group.
        """

        group = self.get_group()

        if group.students.count() >= group.students_limit:

            messages.error(
                self.request,
                _("Crowded group.")
            )

        else:

            group.students.add(student)

            messages.success(
                self.request,
                _("{0} was inserted in the group: {1}"
                  .format(student.get_short_name(), group.title))
            )
