from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grat.models import GRATSubmission
from groups.models import Group
from modules.models import TBLSession
from modules.utils import get_datetimes
from questions.models import Question
from grat.forms import AnswerGRATQuestionForm, GRATDateForm, GRATForm


class GRATView(LoginRequiredMixin,
               PermissionMixin,
               ListView):
    """
    gRAT (Group Readiness Assurance Test)
    """

    template_name = 'grat/grat.html'
    paginate_by = 1
    context_object_name = 'questions'

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'grat_permissions'
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
        Insert discipline, session and form into gRAT context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(GRATView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['date_form'] = GRATDateForm()
        context['grat_form'] = GRATForm()
        context['group'] = self.get_student_group()
        context['submission'] = self.get_group_question_submissions()
        context['form1'] = AnswerGRATQuestionForm(prefix="alternative01")
        context['form2'] = AnswerGRATQuestionForm(prefix="alternative02")
        context['form3'] = AnswerGRATQuestionForm(prefix="alternative03")
        context['form4'] = AnswerGRATQuestionForm(prefix="alternative04")

        return context

    def get_group_question_submissions(self):
        """
        Get the group submission for specific question.
        """

        questions = self.get_queryset()

        page = self.request.GET.get("page")

        if page:
            page = int(page) - 1
        else:
            page = 0

        submission = None

        try:
            submission = GRATSubmission.objects.get(
                session=self.get_session(),
                group=self.get_student_group(),
                question=questions[page]
            )
        except:
            pass

        return submission

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
