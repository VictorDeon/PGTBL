# Django app
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

# Core app

# Ranking app
from groups.models import Group
from disciplines.models import Discipline

class ShowRankingGroupView(LoginRequiredMixin,
                           generic.ListView):

    """
    View to ranking_group .
    """
    model = Group
    template_name = 'rankingGroup/detail.html'
    context_object_name = 'groups'

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

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def get_queryset(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups

    #
    # def get_queryset(self):
    #     return Group.objects.filter(discipline__slug=self.kwargs['slug'])
