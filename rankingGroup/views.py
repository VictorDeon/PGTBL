# Django app
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

# Core app
from core.permissions import PermissionMixin

# Ranking app
from groups.models import Group
from grades.models import Grade
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from rankingGroup.models import Ranking
from rankingGroup.models import GroupInfo


class ShowRankingGroupView(LoginRequiredMixin,
                            PermissionMixin,
                           generic.ListView):

    """
    View to ranking_group .
    """
    model = GroupInfo
    template_name = 'rankingGroup/detail.html'
    context_object_name = 'ranking_of_groups'


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
            ("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline from slug
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_sessions_closed(self):
        """
        Get the closeds tbl sessions from model database.
        """

        discipline = self.get_discipline()
        sessions = []
        try:
            sessions = TBLSession.objects.filter(discipline=discipline,is_closed=True)
        except Exception as e:
            sessions = []


        return sessions


    def set_ranking(self):
        """
        set the list of ranking group
        """

        sessions = self.get_sessions_closed()
        groups = self.get_all_groups_by_discipline()
        ranking = self.get_ranking()

        for s in sessions:
            for group in groups:

                grades = Grade.objects.filter(session=s, group=group)
                sum_grades_irat = 0.0
                sum_grades_pratical = 0.0
                grat = 0.0
                results = 0.0
                try:
                    for grade in grades:
                        sum_grades_pratical += grade.practical
                        sum_grades_irat += grade.irat

                        if not grade.grat == 0:
                            grat = grade.grat
                        sum_grades_irat = sum_grades_irat/len(grades)
                        sum_grades_pratical = sum_grades_pratical/len(grades)

                except ZeroDivisionError:
                    print("Error: There is no grades to assing")
                    messages.error(
                        self.request,"Your TBL session closed without any assingned grades")

                results = sum_grades_irat + grat + sum_grades_pratical

                GroupInfo.objects.update_or_create(ranking=ranking, group=group, results=results)

        list_of_groupsInfo = GroupInfo.objects.filter(ranking=ranking)

        ordered_list = list_of_groupsInfo.order_by('-results')

        return ordered_list


    def get_session_grades(self, session):

        grades = Grade.objects.filter(session=session)

        return grades


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context

    def get_all_groups_by_discipline(self):

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)


        return groups


    def get_ranking(self):

        discipline = self.get_discipline()

        ranking, created = Ranking.objects.update_or_create(
            discipline=discipline,
        )

        return ranking


    def get_queryset(self):
        """
        Get the info_group queryset from model database.
        """
        ranking_of_groups = self.set_ranking()

        counter_list = list(enumerate(ranking_of_groups, 1))

        return counter_list
