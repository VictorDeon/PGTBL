from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages

from core.permissions import PermissionMixin
from core.generics import ObjectRedirectView
from disciplines.models import Discipline

# Get the custom user from settings
User = get_user_model()


class StudentInsertView(LoginRequiredMixin,
                        PermissionMixin,
                        ObjectRedirectView):
    """
    Insert a student or monitor inside discipline by teacher.
    """

    template_name = 'students/users.html'
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
            'disciplines:users',
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

        if user.is_teacher:
            success = self.insert_monitor(user, discipline)
        else:
            success = self.insert_student(user, discipline)

        if success:
            messages.success(
                self.request,
                _("{0} was inserted in the discipline: {1}"
                  .format(user.get_short_name(), discipline.title))
            )

        return redirect(self.get_success_url())

    def insert_monitor(self, user, discipline):
        """
        If user is a teacher, he will have all permission of monitor
        If monitor number is bigger than monitors limit, can't enter.
        """

        if discipline.monitors.count() >= discipline.monitors_limit:
            messages.error(
                self.request,
                _("There are no more vacancies to monitor")
            )

            return False

        if user == discipline.teacher:
            messages.error(
                self.request,
                _("You can't get into your own discipline.")
            )

            return False

        discipline.monitors.add(user)

        return True

    def insert_student(self, user, discipline):
        """
        If user is a student, he will have all permission of student
        If students number is bigger than student limit of discipline, close it
        """

        if discipline.students.count() >= discipline.students_limit:
            if not discipline.is_closed:
                discipline.is_closed = True
                discipline.save()

            messages.error(
                self.request,
                _("Crowded discipline.")
            )

            return False

        discipline.students.add(user)

        return True
