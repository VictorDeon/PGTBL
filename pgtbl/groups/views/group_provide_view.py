from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from core.generics import ObjectRedirectView
from notification.models import Notification


class GroupProvideView(LoginRequiredMixin,
                       PermissionMixin,
                       ObjectRedirectView):
    """
    Make groups available for students.
    """

    template_name = 'groups/list.html'
    permissions_required = ['change_own_group']

    def get_object(self):
        """
        Get discipline by url slug.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

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

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_object()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        if discipline.was_group_provided:
            messages.success(self.request, _("Groups available."))
        else:
            messages.success(self.request, _("Groups unavailable."))

        return success_url

    def action(self, request, *args, **kwargs):
        """
        Change groups permission to available or unavailable.
        """

        discipline = self.get_object()
        title = _("Groups available")
        description = _("Discipline groups available.".format(discipline.title))

        if discipline.was_group_provided:
            discipline.was_group_provided = False
            title = _("Groups unavailable")
            description = _("Discipline groups unavailable.".format(discipline.title))
        else:
            discipline.was_group_provided = True

        discipline.save()

        self.send_notification(discipline, title, description)

        return redirect(self.get_success_url())

    def send_notification(self, discipline, title, description):
        """
        Send notification to all students that the group is available or unavailable.
        """

        for student in discipline.students.all():
            Notification.objects.create(
                title=title,
                description=description,
                sender=discipline.teacher,
                receiver=student,
                discipline=discipline
            )
