from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.contrib import messages
from django.shortcuts import redirect

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession
from exercises.models import ExerciseSubmission, GamificationPointSubmission
from questions.models import Question


class ResetExerciseView(LoginRequiredMixin,
                        PermissionMixin,
                        RedirectView):
    """
    Reset the exercises.
    """

    permissions_required = [
        'show_questions_permission'
    ]

    def get_discipline(self):
        """
        Get discipline by url slug
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_student_group(self):
        """
        Get current student group.
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if self.request.user in group.students.all():
                return group

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        submissions = ExerciseSubmission.objects.filter(
            session=self.get_session(),
            user=self.request.user
        )

        return submissions

    def get_success_url(self):
        """
        Get the success url to redirect to.
        """

        success_url = reverse_lazy(
            'exercises:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url

    def get(self, request, *args, **kwargs):
        """
        Reset exercises list.
        """

        submissions = self.get_queryset()
        questions = Question.objects.filter(session=self.get_session(), is_exercise=True)

        total_score = 0

        if submissions.count() < questions.count():
            total_score -= ((questions.count() - submissions.count()) * 4)

        for submission in submissions:

            if (submission.score > 0):
                total_score += submission.score
            else:
                total_score -= 4

            submission.delete()

        self.insert_gamification_points(total_score)

        messages.success(
            self.request,
            _("Exercise list reseted successfully.")
        )

        return redirect(self.get_success_url())

    def insert_gamification_points(self, total_score):
        """
        Insert gamification point to dashboard
        """

        if self.get_student_group():
            try:
                gamification = GamificationPointSubmission.objects.get(
                    session=self.get_session(),
                    student=self.request.user,
                    group=self.get_student_group()
                )

                gamification.total_score += total_score
                gamification.save()
            except:
                GamificationPointSubmission.objects.create(
                    session=self.get_session(),
                    student=self.request.user,
                    group=self.get_student_group(),
                    total_score=total_score
                )
