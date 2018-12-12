from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from appeals.models import Appeal
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession


class AppealDeleteView(LoginRequiredMixin,
                       PermissionMixin,
                       DeleteView):
    """
    View to delete a specific appeal.
    """

    model = Appeal

    permissions_required = []

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
        Take the session that the appeals belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('session_id', '')
        )

        return session

    def get_object(self):
        """
        Get the specific appeal from tbl session of discipline.
        """

        session = self.get_session()

        appeal = Appeal.objects.get(
            session=session,
            pk=self.kwargs.get('pk', '')
        )

        return appeal

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'appeals:list',
            kwargs={
                'slug': discipline.slug,
                'session_id': session.id
            }
        )

        messages.success(self.request, _("Appeals deleted successfully."))

        return success_url
