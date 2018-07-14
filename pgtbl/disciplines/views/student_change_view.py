from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages

# Core app
from core.permissions import PermissionMixin
from core.generics import ObjectRedirectView
from disciplines.models import Discipline

# Get the custom user from settings
User = get_user_model()


class StudentChangeView(LoginRequiredMixin,
                        PermissionMixin,
                        ObjectRedirectView):
    """
    Change student to monitor or monitor to student if the monitor is no a
    teacher.
    """

    template_name = 'disciplines/students.html'
    permissions_required = [
        'change_own_discipline'
    ]

    def get_object(self):
        """
        Get discipline by url slug
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_object()

        success_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': discipline.slug}
        )

        return success_url

    def action(self, request, *args, **kwargs):
        """
        Insert a user into discipline.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk', '')
        )

        discipline = self.get_object()

        success = self.change_user(user, discipline)

        if success:
            messages.success(self.request, _("Successful modification"))

        return redirect(self.get_success_url())

    def change_user(self, user, discipline):
        """
        Change user to monitor or student.
        """

        if user.is_teacher:
            messages.error(
                self.request,
                _("You can't turn a teacher into a student.")
            )

            return False

        if user in discipline.students.all():
            exceeded = self.monitor_limit_exceeded(discipline)

            if not exceeded:
                discipline.students.remove(user)
                discipline.monitors.add(user)
            else:
                return False
        else:
            exceeded = self.student_limit_exceeded(discipline)

            if not exceeded:
                discipline.monitors.remove(user)
                discipline.students.add(user)
            else:
                return False

        return True

    def student_limit_exceeded(self, discipline):
        """
        Verify if student limit exceeded.
        """

        if discipline.students.count() >= discipline.students_limit:

            messages.error(
                self.request,
                _("Student limit exceeded.")
            )

            return True

        return False

    def monitor_limit_exceeded(self, discipline):
        """
        Verify if monitor limit exceeded.
        """

        if discipline.monitors.count() >= discipline.monitors_limit:

            messages.error(
                self.request,
                _("Monitor limit exceeded.")
            )

            return True

        return False
