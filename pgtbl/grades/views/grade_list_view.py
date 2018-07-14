from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes
from grades.models import Grade


class GradeListView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to see all student grades of TBL sessions.
    """

    template_name = 'grades/list.html'
    context_object_name = 'grades'

    permissions_required = ['show_session_grades']

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the session by url kwargs.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into session context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(GradeListView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        return context

    def get_queryset(self):
        """
        Get the tbl sessions queryset from model database.
        """

        grades = Grade.objects.filter(
            session=self.get_session()
        )

        return grades
