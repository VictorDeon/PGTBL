from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from appeals.forms import AppealForm
from appeals.models import Appeal
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes


class AppealUpdateView(LoginRequiredMixin,
                       PermissionMixin,
                       UpdateView):
    """
    View to update a specific appeal.
    """

    model = Appeal
    template_name = 'appeals/form.html'
    context_object_name = 'appeal'
    form_class = AppealForm

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
        Take the session that the appeal belongs to
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

    def get_context_data(self, **kwargs):
        """
        Insert a discipline and session inside appeal form template.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(AppealUpdateView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('Appeal updated successfully.'))

        return super(AppealUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'appeals:detail',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url