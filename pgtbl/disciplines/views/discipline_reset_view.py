import datetime
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.shortcuts import redirect

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from irat.models import IRATSubmission
from grat.models import GRATSubmission
from exercises.models import ExerciseSubmission
from peer_review.models import PeerReviewSubmission
from grades.models import Grade, FinalGrade
from rank.models import HallOfFameGroup
from rank.utils import get_group_grades


class DisciplineResetView(LoginRequiredMixin,
                          PermissionMixin,
                          DeleteView):

    model = Discipline
    template_name = 'disciplines/details.html'
    permissions_required = [
        'show_discipline_permission',
        'change_own_discipline'
    ]

    def delete(self, request, *args, **kwargs):
        """
        Reset the discipline.
        """

        discipline = self.get_object()

        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': discipline.slug}
        )

        self.reset_discipline(discipline)

        return redirect(redirect_url)

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_groups(self):
        """
        Get all groups in order.
        """

        groups_grade = get_group_grades(self.get_discipline())

        sorted_groups = sorted(groups_grade, key=operator.itemgetter('grade'), reverse=True)

        groups = []
        for group_dict in sorted_groups[:3]:
            group = Group.objects.get(id=group_dict['id'])
            groups.append(group)

        return groups

    def reset_discipline(self, discipline):
        """
        This action will close the discipline, all groups
        and submissions will be deleted and students and
        monitors removed.
        """

        self.create_hall_of_fame(discipline)

        self.modify_discipline_attributes(discipline)

        Group.objects.filter(discipline=discipline).delete()
        FinalGrade.objects.filter(discipline=discipline).delete()

        self.remove_students_and_monitors(discipline)

        for session in discipline.tbl_sessions.all():
            self.modify_tbl_session_attributes(session)

            IRATSubmission.objects.filter(session=session).delete()
            GRATSubmission.objects.filter(session=session).delete()
            PeerReviewSubmission.objects.filter(session=session).delete()
            ExerciseSubmission.objects.filter(session=session).delete()
            Grade.objects.filter(session=session).delete()

    def create_hall_of_fame(self, discipline):
        """
        Create a Hall of Fame with first group of rank.
        """

        group = self.get_groups()[0]

        if Group.objects.count() > 0:

            exists = self.verify_if_hall_of_fame_exists(discipline)

            if exists:
                return None

            hall_of_fame = HallOfFameGroup.objects.create(
                discipline=discipline,
                title=group.title
            )

            for student in group.students.all():
                hall_of_fame.students.add(student)

            hall_of_fame.save()

    def verify_if_hall_of_fame_exists(self, discipline):
        """
        Verify if group in Hall of Fame exists to not duplacate.
        """

        hall_of_fame = HallOfFameGroup.objects.filter(discipline=discipline)

        today = datetime.date.today()

        semester = 1

        if today.month > 8:
            semester = 2

        for group in hall_of_fame:
            if group.get_semester() == semester and group.get_year() == today.year:
                return True

        return False


    def modify_discipline_attributes(self, discipline):
        """
        Close discipline and close groups
        """

        if not discipline.is_closed:
            discipline.is_closed = True

        if discipline.was_group_provided:
            discipline.was_group_provided = False

        discipline.save()

    def modify_tbl_session_attributes(self, session):
        """
        Modify TBL Session attributes
        """

        session.irat_datetime = None
        session.grat_datetime = None
        session.practical_available = False
        session.peer_review_available = False
        session.is_closed = True
        session.is_finished = True
        session.save()

    def remove_students_and_monitors(self, discipline):
        """
        Remove students and monitors from discipline.
        """

        for student in discipline.students.all():
            discipline.students.remove(student)

        for monitor in discipline.monitors.all():
            discipline.monitors.remove(monitor)

        discipline.save()