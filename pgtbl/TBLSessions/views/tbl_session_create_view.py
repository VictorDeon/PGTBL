from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.forms import TBLSessionForm


class TBLSessionCreateView(LoginRequiredMixin,
                           PermissionMixin,
                           CreateView):
    """
    View to insert a new tbl session into the discipline.
    """

    model = TBLSession
    template_name = 'TBLSessions/list.html'
    form_class = TBLSessionForm

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

    def form_valid(self, form):
        """
        Receive the form already validated to create a session.
        """

        form.instance.discipline = self.get_discipline()
        form.save()

        messages.success(self.request, _('TBL session created successfully.'))

        return super(TBLSessionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to form with form errors.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'TBLSessions:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url
