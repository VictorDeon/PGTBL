# Django imports
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (ListView)
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from grades.models import Grade, FinalGrade
from django.db.models import Q

# Application imports
from core.permissions import PermissionMixin
# Get the custom user from settings
from groups.models import Group
from questions.models import Question

User = get_user_model()


class DashboardView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    Show the Dashboard page.
    """

    template_name = 'dashboard/list.html'
    context_object_name = 'dashboard'
    permissions_required = [
        'only_teacher_can_change'
    ]

    def get_discipline(self):
        """
        Get the specific discipline.
        """
        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the group belongs to
        """
        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_groups(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups

    def get_all_students(self):
        """
        Get students from dicipline except the student passed
        """
        discipline = self.get_discipline()

        students = discipline.students.all()

        return students

    def get_exercise_questions(self):
        """
        Get the group queryset from model database.
        """

        this_session = self.get_session()

        questions = Question.objects.filter(session=this_session, is_exercise=True)

        return questions

    def get_RAT_questions(self):
        """
        Get the group queryset from model database.
        """

        this_session = self.get_session()

        questions = Question.objects.filter(session=this_session, is_exercise=False)

        return questions

    def get_context_data(self, **kwargs):
        """
        Insert discipline and session into context data.
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['groups'] = self.get_groups()
        context['students'] = self.get_all_students()
        context['RATQuestions'] = self.get_RAT_questions()
        context['ExerciseQuestions'] = self.get_exercise_questions()

        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """
        session = self.get_session()

        grade = Grade.objects.filter(session=session.id)

        return grade
