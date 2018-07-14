from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.forms import GRATDateForm

# Python imports
from datetime import timedelta


class GRATDateUpdateView(LoginRequiredMixin,
                         PermissionMixin,
                         UpdateView):
    """
    Update the gRAT date.
    """

    model = TBLSession
    template_name = 'questions/grat.html'
    form_class = GRATDateForm

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

        if form.instance.grat_datetime is None:

            messages.error(
                self.request,
                _("gRAT date must to be filled in.")
            )

            return redirect(self.get_success_url())

        if now > form.instance.grat_datetime:

            messages.error(
                self.request,
                _("gRAT date must to be later than today's date.")
            )

            return redirect(self.get_success_url())

        if (form.instance.irat_datetime + timedelta(minutes=form.instance.irat_duration)) > form.instance.grat_datetime:

            messages.error(
                self.request,
                _("gRAT date must to be later than iRAT date with its duration.")
            )

            return redirect(self.get_success_url())

        messages.success(self.request, _('gRAT date updated successfully.'))

        return super(GRATDateUpdateView, self).form_valid(form)

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
