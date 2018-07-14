from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from files.models import DisciplineFile


class DisciplineFileDeleteView(LoginRequiredMixin,
                               PermissionMixin,
                               DeleteView):
    """
    View to delete a specific file.
    """

    model = DisciplineFile

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

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'files:list',
            kwargs={'slug': discipline.slug}
        )

        messages.success(self.request, _("File deleted successfully."))

        return success_url
