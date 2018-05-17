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

class ShowRankingGroupView(LoginRequiredMixin,
                            PermissionMixin,
                           generic.ListView):

    """
    View to ranking_group .
    """
    template_name = 'rankingGroup/detail.html'
    context_object_name = 'groups'

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

        for s in sessions:
            for group in groups:
                sum_grades_irat = 0.0
                grat = 0.0
                grades = Grade.objects.filter(session=s, group=group)

                for grade in grades:
                    sum_grades_irat += grade.irat
                    grat = grade.grat

                sum_grades_irat += grat

                # sum_of_grades = sum(grade.irat for grade in grades)
                groups_add_grades.append({
                    'group':group,
                    'iratSet':sum_grades_irat,
                })

        return groups_add_grades


    def get_session_grades(self, session):

        grades = Grade.objects.filter(session=session)


        # groups = self.get_queryset()
        # for g in groups:
        #     grade = Grade.objects.filter(session=session,group=g).get('grat')
        #     grades.append(grade)

        return grades


    # def get_groups(self):
    #
    #     groups = []
    #
    #     grades = self.get_session_grades()
    #
    #     for g in grade:
    #         groups.append(g.group)
    #
    #     return groups





    # def get_groups_grades(self, grades):
    #
    #     grupos = []
    #
    #     for grade in grades:
    #         grupos.append([grade.group],[grade.grat])
    #
    #     return grupos


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        # context['sessions'] = self.get_sessions_closed()
        #context['grades'] = self.get_session_grades(self.get_sessions_closed()[0])
        context['groups_add_grades']=self.get_alog()

        return context

    def get_all_groups_by_discipline(self):

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups

    def get_queryset(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups
