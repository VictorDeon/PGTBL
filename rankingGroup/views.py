# Django app
from django.views import generic
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

# Core app
from core.permissions import PermissionMixin

# Ranking app
from groups.models import Group
from grades.models import Grade
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from .models import Ranking

from operator import attrgetter


class ShowRankingGroupView(LoginRequiredMixin,
                            PermissionMixin,
                           generic.ListView):

    """
    View to ranking_group .
    """
    model = Ranking
    template_name = 'rankingGroup/detail.html'
    context_object_name = 'info_query'
    ordering = ['sum_results_sessions']


    # Permissions
    permissions_required = [
        'show_discipline_groups_permission'
    ]

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

    def get_sessions_closed(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        sessions = TBLSession.objects.filter(discipline=discipline,is_closed=True)

        return sessions


    def get_alog(self):

        sessions = self.get_sessions_closed()
        groups = self.get_all_groups_by_discipline()
        groups_add_grades = []
        list_update = []

        for s in sessions:
            for group in groups:
                sum_grades_irat = 0.0
                sum_grades_pratical = 0.0
                grat = 0.0
                sum_results = 0.0
                grades = Grade.objects.filter(session=s, group=group)

                for grade in grades:
                    sum_grades_pratical += grade.practical
                    sum_grades_irat += grade.irat
                    grat = grade.grat


                sum_grades_irat = sum_grades_irat/len(grades)
                sum_grades_pratical = sum_grades_pratical/len(grades)

                sum_results = sum_grades_irat + grat + sum_grades_pratical

                groups_add_grades.append({
                    'group':group,
                    'sum_results_sessions':sum_results,
                })

        list_update = sorted(groups_add_grades,key=lambda K: K.get('sum_results_sessions'), reverse=True)

        return list_update


    def get_session_grades(self, session):

        grades = Grade.objects.filter(session=session)

        return grades


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['groups_add_grades']=self.get_alog()

        return context

    def get_all_groups_by_discipline(self):

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups


    def get_queryset(self):
        """
        Get the info_group queryset from model database.
        """

        info_query = self.get_alog()

        return info_query
