from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from files.models import ModuleFile
from files.forms import ModuleFileForm


class ModuleFileCreateView(LoginRequiredMixin,
                           PermissionMixin,
                           CreateView):
    """
    View to insert a new file into the tbl session.
    """

    model = ModuleFile
    template_name = 'files/session-list.html'
    form_class = ModuleFileForm

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

    def get_session(self):
        """
        Take the session that the file belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def form_valid(self, form):
        """
        Receive the form already validated to create a file.
        """

        form.instance.discipline = self.get_discipline()
        form.instance.session = self.get_session()
        form.save()

        messages.success(self.request, _('File created successfully.'))

        return super(ModuleFileCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to form with form error.
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
        session = self.get_session()

        success_url = reverse_lazy(
            'files:module-list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url
