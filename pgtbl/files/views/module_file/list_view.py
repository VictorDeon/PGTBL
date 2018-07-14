from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes
from files.models import ModuleFile
from files.forms import ModuleFileForm


class ModuleFileListView(LoginRequiredMixin,
                         PermissionMixin,
                         ListView):
    """
    View to see all tbl session file of discipline.
    """

    template_name = 'files/session_list.html'
    paginate_by = 10
    context_object_name = 'files'

    # Modificar
    permissions_required = [
        'show_files_permission',
        'show_tbl_file_session'
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

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session and form into file context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(ModuleFileListView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['form'] = ModuleFileForm()

        return context

    def get_queryset(self):
        """
        Get the files queryset from model database.
        """

        session = self.get_session()

        # Modificar
        files = ModuleFile.objects.filter(
            session=session
        )

        return files
