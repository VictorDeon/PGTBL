from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes


class PracticalTestDetailView(LoginRequiredMixin,
                              PermissionMixin,
                              DetailView):
    """
    View to show the practical test.
    """

    template_name = 'TBLSessions/practical_test.html'
    context_object_name = 'session'

    permissions_required = [
        'show_tbl_session',
        'show_practical_test',
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
            'TBLSessions:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_object(self):
        """
        Get the session discipline.
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline into tbl session context.
        """

        session = self.get_object()
        irat_datetime, grat_datetime = get_datetimes(session)

        context = super(PracticalTestDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime

        return context
