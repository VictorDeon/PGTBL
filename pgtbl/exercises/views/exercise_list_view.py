from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from exercises.forms.exercise_form import ExerciseForm
from modules.models import TBLSession
from modules.utils import get_datetimes
from questions.models import Question
from questions.forms import AnswerQuestionForm

from django.core.cache import cache

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
        context['form'] = ExerciseForm()
        context['form1'] = AnswerQuestionForm(prefix="alternative01")
        context['form2'] = AnswerQuestionForm(prefix="alternative02")
        context['form3'] = AnswerQuestionForm(prefix="alternative03")
        context['form4'] = AnswerQuestionForm(prefix="alternative04")

        questions = self.get_queryset()
        context['paginator'] = Paginator(questions, 1)

        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        BUG: Pagination buttons in template
        """

        session = self.get_session()

        random_questions = Question.objects.filter(
            session=session,
            is_exercise=True
        ).order_by('?')[:10]

        questions = cache.get('questions')

        if not questions:
            cache.set('questions', random_questions)
            questions = cache.get('questions')

        return questions