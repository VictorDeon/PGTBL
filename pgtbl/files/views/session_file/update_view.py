from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes
from files.models import SessionFile
from files.forms import SessionFileForm


class SessionFileUpdateView(LoginRequiredMixin,
                            PermissionMixin,
                            UpdateView):
    """
    View to update a specific session file.
    """

    model = SessionFile
    template_name = 'files/session_form.html'
    context_object_name = 'file'
    form_class = SessionFileForm

    permissions_required = [
        'monitor_can_change'
    ]

    def get_discipline(self):
        """
        Take the discipline that the file belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the file belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Get the specific file from tbl session of discipline.
        """

        session = self.get_session()

        archive = SessionFile.objects.get(
            session=session,
            pk=self.kwargs.get('file_id', '')
        )

        return archive

    def get_context_data(self, **kwargs):
        """
        Insert a discipline and session inside file form template.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(SessionFileUpdateView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('File updated successfully.'))

        return super(SessionFileUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'files:session-list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url
