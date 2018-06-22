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
from questions.models import Question, IRATSubmission, GRATSubmission

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
        session = TBLSession.objects.get(
            Q(discipline=self.get_discipline()),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_groups(self):
        """
        Get the group queryset from model database.
        """
        groups = Group.objects.filter(discipline=self.get_discipline())

        data = {}
        for counter, group in enumerate(groups):
            data[counter] = group.title

        return data

    def get_all_students(self):
        """
        Get students from dicipline except the student passed
        """
        data = {}
        for counter, student in enumerate(self.get_discipline().students.all()):
            data[counter] = student.username

        return data

    def get_questions(self, type):
        questions = Question.objects.filter(session=self.get_session(), is_exercise=type)

        data = {}
        for counter, question in enumerate(questions):
            data[counter] = question.title

        return data

    def get_iRAT_submissions(self):
        submissions = IRATSubmission.objects.filter(session=self.get_session())

        data = {}
        for counter, submission in enumerate(submissions):
            data[3*counter] = submission.user.username
            data[3*counter+1] = submission.question.title
            data[3*counter+2] = submission.score

        return data

    def get_iRAT_total(self):
        questions = Question.objects.filter(session=self.get_session(), is_exercise=False)

        data = {}
        for counter, question in enumerate(questions):
            submissions = IRATSubmission.objects.filter(question=question)
            score = 0
            for submission in submissions:
                score += submission.score
            data[counter] = score

        return data

    def get_gRAT_submissions(self):
        """
        Get the group queryset from model database.
        """
        submissions = GRATSubmission.objects.filter(session=self.get_session())

        data = {}
        for counter, submission in enumerate(submissions):
            data[3*counter] = submission.group.title
            data[3*counter+1] = submission.question.title
            data[3*counter+2] = submission.score

        return data

    def get_gRAT_total(self):
        questions = Question.objects.filter(session=self.get_session(), is_exercise=False)

        data = {}
        for counter, question in enumerate(questions):
            submissions = GRATSubmission.objects.filter(question=question)
            score = 0
            for submission in submissions:
                score += submission.score
            data[counter] = score

        return data

    def get_peer_review_grades(self):
        students = self.get_discipline().students.all()

        data = {}
        for counter, student in enumerate(students):
            grades = Grade.objects.filter(session=self.get_session(), student=student)
            data[2 * counter] = student.username
            if grades:
                for grade in grades:
                    data[2*counter+1] = grade.peer_review
            else:
                data[2*counter+1] = 0

        return data

    def get_rat_average(self):
        grades = Grade.objects.filter(session=self.get_session())

        data = {}
        score = 0
        for counter, grade in enumerate(grades):
            score += grade.irat

        students = self.get_discipline().students.all()
        data['iRAT'] = score / students.count()

        score = 0
        for counter, grade in enumerate(grades):
            score += grade.grat

        groups = Group.objects.filter(discipline=self.get_discipline())
        data['gRAT'] = score / groups.count()

        return data

    def get_context_data(self, **kwargs):
        """
        Insert info into context data.
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['groups'] = self.get_groups()
        context['students'] = self.get_all_students()
        context['iRATSubmissions'] = self.get_iRAT_submissions()
        context['gRATSubmissions'] = self.get_gRAT_submissions()
        context['iRATTotalScore'] = self.get_iRAT_total()
        context['gRATTotalScore'] = self.get_gRAT_total()
        context['PeerReviewGrades'] = self.get_peer_review_grades()
        context['RATQuestions'] = self.get_questions(False)
        context['ExerciseQuestions'] = self.get_questions(True)
        context['RATAverage'] = self.get_rat_average()

        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """
        session = self.get_session()

        grade = Grade.objects.filter(session=session)

        return grade
