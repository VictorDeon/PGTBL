from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes
from grades.models import Grade
from groups.models import Group
from questions.models import Question
from irat.models import IRATSubmission


class IRATResultView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    Show the result of iRAT test.
    """

    template_name = 'irat/result.html'
    context_object_name = 'submissions'

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'show_test_result'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("The results only be available when gRAT is done.")
        )

        failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
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

    def get_questions(self):
        """
        Get all exercises list questions.
        """

        questions = Question.objects.filter(
            session=self.get_session(),
            is_exercise=False
        )

        return questions

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

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session into iRAT result context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(IRATResultView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['result'] = self.result()

        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        submissions = IRATSubmission.objects.filter(
            session=self.get_session(),
            user=self.request.user
        )

        return submissions

    def result(self):
        """
        Get the total scores about iRAT.
        """

        questions = self.get_questions()
        submissions = self.get_queryset()

        score = 0
        grade = 0

        total = 4 * questions.count()

        for submission in submissions:
            score += submission.score

        if total > 0:
            grade = (score / total) * 10

        self.create_grade(grade)

        result = {
            'score': score,
            'total': total,
            'grade': "{0:.2f}".format(grade)
        }

        return result

    def create_grade(self, grade):
        """
        Create a grade for specific student
        """

        discipline = self.get_discipline()

        grades = Grade.objects.filter(
            session=self.get_session(),
            student=self.request.user
        )

        if grades.count() == 0 and self.request.user in discipline.students.all():
            Grade.objects.create(
                session=self.get_session(),
                student=self.request.user,
                group=self.get_student_group(),
                irat=grade
            )
