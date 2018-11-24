from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from exercises.models import GamificationPointSubmission
from modules.models import TBLSession


class ReportDetailView(LoginRequiredMixin,
                       PermissionMixin,
                       DetailView):
    """
    View to show the teacher dashboard.
    """

    template_name = 'dashboard/report.html'
    context_object_name = 'report'

    permissions_required = ['show_report_permission']

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

        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        return context

    def get_object(self, queryset=None):
        """
        Get gamification students points
        """

        gamification = GamificationPointSubmission.objects.filter(
            session=self.get_session()
        )

        return gamification
