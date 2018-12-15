from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from appeals.models import Appeal
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes


class AppealListView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    View to see all tbl session appeals
    """

    template_name = 'appeals/list.html'
    paginate_by = 10
    context_object_name = 'appeals'

    permissions_required = ['show_appeals']

    def get_discipline(self):
        """
        Take the discipline that the appeal belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the appeal belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('session_id', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert some attributes into appeal context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(AppealListView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        return context

    def get_queryset(self):
        """
        Get the appeals queryset from model database.
        """

        session = self.get_session()

        appeals = Appeal.objects.filter(
            session=session
        )

        appeals = self.search_appeals(appeals)

        return appeals

    def search_appeals(self, appeals):
        """
        Search specific appeal by title or question name
        """

        query = self.request.GET.get("q_info")

        if query:
            # Verify if appeal title and question name contains the query specify
            # by user and filter all appeals that satisfies this
            appeals = appeals.filter(
                Q(title__icontains=query) |
                Q(question__title__icontains=query)
            ).distinct()

        return appeals

