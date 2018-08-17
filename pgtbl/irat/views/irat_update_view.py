from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from irat.forms import IRATForm


class IRATUpdateView(LoginRequiredMixin,
                     PermissionMixin,
                     UpdateView):
    """
    Update the iRAT duration and weight
    """

    model = TBLSession
    template_name = 'irat/irat.html'
    form_class = IRATForm

    # Permissions
    permissions_required = ['crud_tests']

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('iRAT updated successfully.'))

        return super(IRATUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'irat:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url
