from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from files.models import SessionFile


class SessionFileDeleteView(LoginRequiredMixin,
                            PermissionMixin,
                            DeleteView):
    """
    View to delete a specific tbl session file.
    """

    model = SessionFile

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

        messages.success(self.request, _("File deleted successfully."))

        return success_url
