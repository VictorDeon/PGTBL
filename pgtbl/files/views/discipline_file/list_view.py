from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from files.models import DisciplineFile
from files.forms import DisciplineFileForm


class DisciplineFileListView(LoginRequiredMixin,
                             PermissionMixin,
                             ListView):
    """
    View to see all file of discipline.
    """

    template_name = 'files/discipline/list.html'
    paginate_by = 10
    context_object_name = 'files'

    permissions_required = [
        'show_files_permission'
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
        Insert discipline and form into file context data.
        """

        context = super(DisciplineFileListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = DisciplineFileForm()
        return context

    def get_queryset(self):
        """
        Get the files queryset from model database.
        """

        discipline = self.get_discipline()

        files = DisciplineFile.objects.filter(discipline=discipline)

        return files
