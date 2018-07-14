from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.views.generic import UpdateView

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes
from modules.forms import PracticalTestForm


class PracticalTestUpdateView(LoginRequiredMixin,
                              PermissionMixin,
                              UpdateView):
    """
    View to update the practical test.
    """

    model = TBLSession
    template_name = 'practical_test/update.html'
    context_object_name = 'session'
    form_class = PracticalTestForm

    permissions_required = [
        'monitor_can_change_if_is_teacher',
        'show_tbl_session'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
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
        Insert a discipline inside tbl session form template.
        """

        session = self.get_object()
        irat_datetime, grat_datetime = get_datetimes(session)

        context = super(PracticalTestUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime

        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('Practical test updated successfully.'))

        return super(PracticalTestUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'modules:practical-details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url
