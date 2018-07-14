from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.forms import GRATForm


class GRATUpdateView(LoginRequiredMixin,
                     PermissionMixin,
                     UpdateView):
    """
    Update the gRAT duration and weight
    """

    model = TBLSession
    template_name = 'grat/grat.html'
    form_class = GRATForm

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

        messages.success(self.request, _('gRAT updated successfully.'))

        return super(GRATUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'questions:grat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url
