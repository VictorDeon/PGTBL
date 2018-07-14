from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from files.models import DisciplineFile
from files.forms import DisciplineFileForm


class DisciplineFileCreateView(LoginRequiredMixin,
                               PermissionMixin,
                               CreateView):
    """
    View to insert a new file into the discipline.
    """

    model = DisciplineFile
    template_name = 'files/discipline/list.html'
    form_class = DisciplineFileForm

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

    def form_valid(self, form):
        """
        Receive the form already validated to create a file.
        """

        form.instance.discipline = self.get_discipline()
        form.save()

        messages.success(self.request, _('File created successfully.'))

        return super(DisciplineFileCreateView, self).form_valid(form)

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

        success_url = reverse_lazy(
            'files:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url
