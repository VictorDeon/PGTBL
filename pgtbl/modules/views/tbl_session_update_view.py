from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.forms import TBLSessionForm


class TBLSessionUpdateView(LoginRequiredMixin,
                           PermissionMixin,
                           UpdateView):
    """
    View to update a specific tbl session.
    """

    model = TBLSession
    template_name = 'modules/form.html'
    context_object_name = 'session'
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

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside tbl session form template.
        """

        context = super(TBLSessionUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('TBL session updated successfully.'))

        if not form.instance.is_closed:
            form.instance.is_finished = False

        return super(TBLSessionUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'modules:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url
