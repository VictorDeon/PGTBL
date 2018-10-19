from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.shortcuts import redirect

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from grades.models import Grade
from groups.models import Group
from peer_review.models import PeerReviewSubmission


class TBLSessionFinishView(LoginRequiredMixin,
                           PermissionMixin,
                           DeleteView):

    model = TBLSession
    template_name = 'modules/details.html'
    permissions_required = ['only_teacher_can_change']

    def get_discipline(self):
        """
        Get the TBL session discipline.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def delete(self, request, *args, **kwargs):
        """
        Finish the TBL session.
        """

        discipline = self.get_discipline()
        session = self.get_object()

        redirect_url = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        if not session.is_finished:
            session.is_finished = True
            session.is_closed = True

            for student in discipline.students.all():
                peer_review_grade = self.calcule_peer_review_grade(student)
                self.update_grade(student, peer_review_grade)

            self.calcule_gamification_bonus()

        session.save()

        return redirect(redirect_url)

    def calcule_gamification_bonus(self):
        """
        Calcule gamification bonus
        """

        session = self.get_object()
        group_winner = self.get_group_gamification_winner()

        grades = Grade.objects.filter(
            session=session,
            group=group_winner
        )

        for grade in grades:
            grade.session_grade += session.exercise_score
            grade.save()

    def get_group_gamification_winner(self):
        """
        Calcule gamification score points to get the group winner
        """

        groups = Group.objects.filter(discipline=self.get_discipline())
        session = self.get_object()

        group_winner = groups.first()
        winner = 0

        for group in groups:
            total_score = 0
            
            for submission in GamificationPointSubmission.objects.filter(session=session, group=group):
                total_score += submission.total_score

            if total_score > winner:
                winner = total_score
                group_winner = group

        return group_winner

    def calcule_peer_review_grade(self, student):
        """
        Calcule the peer review grade of session students
        """

        peer_review_grade = 0

        submissions = PeerReviewSubmission.objects.filter(
            session=self.get_object(),
            student=student
        )

        for submission in submissions:
            peer_review_grade += submission.score

        group = self.get_student_group(student)
        group_length = group.students.count() - 1

        peer_review_grade = (peer_review_grade / group_length) / 10

        return peer_review_grade

    def get_student_group(self, student):
        """
        Get the student group length

        :return: Group length
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if student in group.students.all():
                return group

    def update_grade(self, student, peer_review_grade):
        """
        Update the student grade with peer review grade.

        :param student: Student grade to be updated
        :param peer_review_grade: Peer Review grade
        """

        try:
            grade = Grade.objects.get(
                session=self.get_object(),
                student=student
            )

            if grade.peer_review == 0:
                grade.peer_review = peer_review_grade
                grade.save()
        except:
            Grade.objects.create(
                session=self.get_object(),
                student=student,
                group=self.get_student_group(student),
                peer_review=peer_review_grade
            )
