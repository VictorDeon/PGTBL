from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from files.models import DisciplineFile
from files.forms import DisciplineFileForm


class DisciplineFileUpdateView(LoginRequiredMixin,
                               PermissionMixin,
                               UpdateView):
    """
    View to update a specific file.
    """

    model = DisciplineFile
    template_name = 'files/discipline/form.html'
    context_object_name = 'file'
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

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside file form.
        """

        context = super(DisciplineFileUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('File updated successfully.'))

        return super(DisciplineFileUpdateView, self).form_valid(form)

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
