# Django app
from django.views import generic
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

# Core app
from core.permissions import PermissionMixin

# Ranking app
from groups.models import Group
from disciplines.models import Discipline
from TBLSessions.models import TBLSession

class ShowRankingGroupView(LoginRequiredMixin,
                            PermissionMixin,
                           generic.ListView):

    """
    View to ranking_group .
    """
    model = Group
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

    def get_sessions(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        sessions = TBLSession.objects.filter(discipline=discipline)

        return sessions


    # def verify_status_sessions(self):
    #
    #     sessions = self.get_sessions()
    #
    #     grades = []
    #
    #     for session in sessions:
    #         if session.is_closed:
    #             grades = session.grades.all()
    #
    #     return grades
    #
    # def get_groups_grade(self):
    #
    #     grades = verify_status_session()




    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['sessions'] = self.get_sessions()
        # context['grades'] = self.verify_status_session()

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
