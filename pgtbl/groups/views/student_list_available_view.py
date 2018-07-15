from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group


class StudentListAvailableView(LoginRequiredMixin,
                               PermissionMixin,
                               ListView):
    """
    Show a list of students available to insert into groups.
    """

    template_name = 'groups/students.html'
    paginate_by = 12
    context_object_name = 'students'
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
            pk=self.kwargs.get('pk', '')
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

    def get_queryset(self):
        """
        List all available students to insert into discipline.
        """

        self.discipline = self.get_discipline()
        students = self.discipline.students.all()

        students_available = []

        for student in students:
            available = self.is_available(student)

            if available is True:
                students_available.append(student)

        return students_available

    def is_available(self, student):
        """
        Scroll through the discipline groups and return True if it is not
        in any group.
        """

        available = False

        for group in self.discipline.groups.all():
            if student in group.students.all():
                available = False
                break
            else:
                available = True

        return available

    def get_context_data(self, **kwargs):
        """
        Insert discipline and group instance into student list.
        """

        context = super(StudentListAvailableView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['group'] = self.get_group()

        return context
