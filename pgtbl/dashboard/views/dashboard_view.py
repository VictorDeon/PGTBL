from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from exercises.models import GamificationPointSubmission
from groups.models import Group
from modules.models import TBLSession

import operator


class DashboardDetailView(LoginRequiredMixin,
                          PermissionMixin,
                          DetailView):
    """
    View to show the group dashboard.
    """

    template_name = 'dashboard/dashboard.html'
    context_object_name = 'gamification'

    permissions_required = ['show_dashboard_permission']

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the dashboard belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['group'] = self.get_student_group()
        context['total_score'] = self.get_total_points()
        context['average'] = self.get_average()
        context['winner_points'] = self.get_student_group_position()['winner_points']
        context['position'] = self.get_student_group_position()['position']
        context['badges'] = self.get_badges()

        return context

    def get_student_group(self):
        """
        Get specific group.
        """

        discipline = self.get_discipline()
        student = self.request.user

        groups = Group.objects.filter(discipline=discipline)

        for group in groups:
            if student in group.students.all():
                return group

        return None

    def get_object(self, queryset=None):
        """
        Get gamification students points
        """

        gamification = GamificationPointSubmission.objects.filter(
            session=self.get_session(),
            group=self.get_student_group()
        )

        return gamification

    def get_badges(self):
        """
        Get total points to visualize badges.
        """

        gamifications = GamificationPointSubmission.objects.filter(
            group=self.get_student_group()
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
            'total_score': total_score,
            'first_position': first_position,
            'always_first_position': always_first_position
        }

        return result

    def get_total_points(self):
        """
        Calcule total points of group
        """

        gamification = self.get_object()

        total_score = 0

        for submission in gamification:
            total_score += submission.total_score

        return total_score

    def get_average(self):
        """
        Get the group point average.
        """

        group = self.get_student_group()

        average = self.get_total_points() / group.students.count()

        return average

    def get_groups_gamification(self):
        """
        Get groups positions
        """

        groups = Group.objects.filter(discipline=self.get_discipline())

        groups_position = []
        for group in groups:
            total_score = 0

            for submission in group.point_submissions.all():
                if submission.session == self.get_session():
                    total_score += submission.total_score

            group = {
                'id': group.id,
                'title': group.title,
                'total_score': total_score
            }

            groups_position.append(group)

        return groups_position

    def get_student_group_position(self):
        """
        Get the current group student position.
        """

        groups = self.get_groups_gamification()
        sorted_groups = sorted(groups, key=operator.itemgetter('total_score'), reverse=True)

        position = 1
        winner_points = 0

        for group in sorted_groups:
            if group['id'] == self.get_student_group().id:
                break

            position += 1
            winner_points = group['total_score'] - self.get_total_points()

        group = {
            'position': position,
            'winner_points': winner_points
        }

        return group

