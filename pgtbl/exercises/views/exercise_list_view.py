from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes
from questions.models import Question
from questions.forms import AnswerQuestionForm

from random import shuffle

class ExerciseListView(LoginRequiredMixin,
                       PermissionMixin,
                       ListView):
    """
    View to see all the questions that the students will answer.
    """

    template_name = 'exercises/list.html'
    paginate_by = 1
    context_object_name = 'questions'

    # Permissions
    permissions_required = [
        'show_questions_permission'
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

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session and form into exercises list context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(ExerciseListView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['form1'] = AnswerQuestionForm(prefix="alternative01")
        context['form2'] = AnswerQuestionForm(prefix="alternative02")
        context['form3'] = AnswerQuestionForm(prefix="alternative03")
        context['form4'] = AnswerQuestionForm(prefix="alternative04")

        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        session = self.get_session()

        questions = Question.objects.filter(
            session=session,
            is_exercise=True
        )

        return questions