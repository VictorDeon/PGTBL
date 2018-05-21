# Django app
from django.views import generic
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

# Core app
from core.permissions import PermissionMixin

# Ranking app
from groups.models import Group
from grades.models import Grade
from disciplines.models import Discipline
from TBLSessions.models import TBLSession


class ShowRankingGroupView(LoginRequiredMixin,
                            PermissionMixin,
                           generic.ListView):

    """
    View to ranking_group .
    """
    template_name = 'rankingGroup/detail.html'
    context_object_name = 'groups_with_grades_results'

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

        sessions = TBLSession.objects.filter(discipline=discipline,is_closed=True)

        return sessions


    def set_ranking(self):
        """
        set the list of ranking group
        """

        sessions = self.get_sessions_closed()
        groups = self.get_all_groups_by_discipline()
        groups_with_grades_results = []
        list_update = []
        new_list = []

        for s in sessions:
            for group in groups:

                grades = Grade.objects.filter(session=s, group=group)
                sum_grades_irat = 0.0
                sum_grades_pratical = 0.0
                grat = 0.0
                sum_all_results = 0.0

                for grade in grades:
                    sum_grades_pratical += grade.practical
                    sum_grades_irat += grade.irat

                    if not grade.grat == 0:
                        grat = grade.grat

                sum_grades_irat = sum_grades_irat/len(grades)
                sum_grades_pratical = sum_grades_pratical/len(grades)

                try:
                    sum_grades_irat = sum_grades_irat/len(grades)
                    sum_grades_pratical = sum_grades_pratical/len(grades)
                except ZeroDivisionError:
                    print("Error: There is no grades to assing")
                    messages.error(
                        self.request,"Your TBL session closed without any assingned grades")

                sum_all_results = sum_grades_irat + grat + sum_grades_pratical

                groups_with_grades_results.append({
                    'group':group,
                    'sum_results_sessions':sum_all_results,
                })

        list_update = sorted(groups_with_grades_results,key=lambda K: K.get('sum_results_sessions'), reverse=True)

        i = 1
        for update in list_update:
            new_list.append({
                'group_position': i,
                'group_info':update,
            })
            i = i + 1

        return new_list


    def get_session_grades(self, session):

        grades = Grade.objects.filter(session=session)

        return grades


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['groups_add_grades']=self.set_ranking()

        return context

    def get_all_groups_by_discipline(self):

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups


    def get_queryset(self):
        """
        Get the info_group queryset from model database.
        """

        ranking = self.set_ranking()

        return ranking
