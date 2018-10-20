from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from exercises.models import GamificationPointSubmission
from groups.models import Group
from modules.models import TBLSession


class DashboardDetailView(LoginRequiredMixin,
                          PermissionMixin,
                          DetailView):
    """
    View to show the group dashboard.
    """

    template_name = 'dashboard/dashboard.html'
    context_object_name = 'group'

    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the dashboard belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def get_object(self):
        """
        Get specific group.
        """

        discipline = self.get_discipline()
        student = self.request.user

        groups = Group.objects.filter(discipline=discipline)

        for group in groups:
            if student in group.students.all():
                return group

        return None

