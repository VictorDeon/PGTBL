from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from exercises.models import GamificationPointSubmission
from groups.models import Group
from rank.utils import get_group_grades

import operator


class GroupRankView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to show the group rank.
    """

    template_name = 'rank/group_rank.html'
    context_object_name = 'results'

    permissions_required = ['show_rank_permission']

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

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

        context = super(GroupRankView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def get_queryset(self):
        """
        Get all groups.
        """

        groups_grade = get_group_grades(self.get_discipline())

        sorted_groups = sorted(groups_grade, key=operator.itemgetter('grade'), reverse=True)

        results = []
        for group_dict in sorted_groups[:3]:
            group = Group.objects.get(id=group_dict['id'])
            result = self.get_badges(group)
            results.append(result)

        print(results)

        return results

    def get_badges(self, group):
        """
        Get total points to visualize badges.
        """

        gamifications = GamificationPointSubmission.objects.filter(
            group=group
        )

        total_score = 0
        first_position = False
        always_first_position = True

        for gamification in gamifications:
            if gamification.first_position:
                first_position = True
            else:
                always_first_position = False

            total_score += gamification.total_score

        if not gamifications:
            always_first_position = False

        result = {
            'group': group,
            'total_score': total_score,
            'first_position': first_position,
            'always_first_position': always_first_position
        }

        return result


