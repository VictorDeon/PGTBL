from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession


class TBLSessionDeleteView(LoginRequiredMixin,
                           PermissionMixin,
                           DeleteView):
    """
    View to delete a specific tbl session.
    """

    model = TBLSession

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'modules:list',
            kwargs={'slug': discipline.slug}
        )

        messages.success(self.request, _("TBL session deleted successfully."))

        return success_url
