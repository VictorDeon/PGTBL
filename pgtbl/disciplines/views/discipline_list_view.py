from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.utils import order
from disciplines.models import Discipline
from disciplines.forms import DisciplineEnterForm


class DisciplineListView(LoginRequiredMixin, ListView):
    """
    View to search a discipline and enter it.
    """

    template_name = 'disciplines/list.html'
    paginate_by = 10
    context_object_name = 'disciplines'

    def get_context_data(self, **kwargs):
        """
        Insert a form inside discipline list.
        """

        context = super(DisciplineListView, self).get_context_data(**kwargs)
        context['form'] = DisciplineEnterForm()
        return context

    def get_queryset(self):
        """
        Get the discipline queryset from model database.
        """

        user = self.request.user

        # Disciplines available for user
        queryset = Discipline.objects.available(user)

        queryset = order(self, queryset)

        queryset = self.search_disciplines(queryset)

        return queryset

    def search_disciplines(self, disciplines):
        """
        Search from disciplines a specific discipline.
        """

        # From url after search get the ?q_info=...
        query = self.request.GET.get("q_info")
        if query:
            disciplines = Discipline.objects.search(query)

        return disciplines
