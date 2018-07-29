from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes
from questions.models import Question
from exercises.models import ExerciseSubmission


class ExerciseResultView(LoginRequiredMixin,
                         PermissionMixin,
                         ListView):
    """
    Show the result of exercises list.
    """

    template_name = 'exercises/result.html'
    context_object_name = 'submissions'

    # Permissions
    permissions_required = [
        'show_questions_permission',
    ]

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
            is_exercise=True
        )

        return questions

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session into exercises result context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(ExerciseResultView, self).get_context_data(**kwargs)
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

        submissions = ExerciseSubmission.objects.filter(
            session=self.get_session(),
            user=self.request.user
        )

        return submissions

    def result(self):
        """
        Get the total scores about exercises list.
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

        result = {
            'score': score,
            'total': total,
            'grade': "{0:.2f}".format(grade)
        }

        return result
