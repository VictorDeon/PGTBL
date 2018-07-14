from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.forms import IRATDateForm


class IRATDateUpdateView(LoginRequiredMixin,
                         PermissionMixin,
                         UpdateView):
    """
    Update the iRAT date.
    """

    model = TBLSession
    template_name = 'questions/irat.html'
    form_class = IRATDateForm

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

        now = timezone.localtime(timezone.now())

        if form.instance.irat_datetime is None:

            messages.error(
                self.request,
                _("iRAT date must to be filled in.")
            )

            return redirect(self.get_success_url())

        if now > form.instance.irat_datetime:

            messages.error(
                self.request,
                _("iRAT date must to be later than today's date.")
            )

            return redirect(self.get_success_url())

        messages.success(self.request, _('iRAT date updated successfully.'))

        return super(IRATDateUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'questions:irat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url
