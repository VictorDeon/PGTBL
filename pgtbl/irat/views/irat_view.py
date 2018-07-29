from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes
from questions.models import Question
from questions.forms import AnswerQuestionForm
from irat.forms import IRATDateForm, IRATForm


class IRATView(LoginRequiredMixin,
               PermissionMixin,
               ListView):
    """
    iRAT (Individual Readiness Assurance Test)
    """

    template_name = 'irat/irat.html'
    paginate_by = 1
    context_object_name = 'questions'

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'irat_permissions'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
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

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session and form into exercises list context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(IRATView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['date_form'] = IRATDateForm()
        context['irat_form'] = IRATForm()
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
            is_exercise=False
        )

        return questions
