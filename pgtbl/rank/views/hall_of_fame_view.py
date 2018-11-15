from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from rank.models import HallOfFameGroup


class HallOfFameView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    View to show the hall of fame.
    """

    template_name = 'rank/hall_of_fame.html'
    paginate_by = 3
    context_object_name = 'hall_of_fame'

    permissions_required = ['show_hall_of_fame']

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(HallOfFameView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context

    def get_queryset(self):
        """
        Get all groups.
        """

        groups = HallOfFameGroup.objects.filter(
            discipline=self.get_discipline()
        )

        queryset = self.search_group(groups)

        return queryset

    def search_group(self, groups):
        """
        Search for a specific group.
        """

        query = self.request.GET.get("q_info")

        if query:
            groups = groups.filter(title__icontains=query)

        return groups