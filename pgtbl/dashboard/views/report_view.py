from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grat.models import GRATSubmission
from irat.models import IRATSubmission
from modules.models import TBLSession
from questions.models import Question


class ReportDetailView(LoginRequiredMixin,
                       PermissionMixin,
                       DetailView):
    """
    View to show the teacher dashboard.
    """

    template_name = 'dashboard/report.html'
    context_object_name = 'question_data'

    permissions_required = ['show_report_permission']

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the dashboard belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['questions_options'] = self.get_options(
            title="Number of correct answers for questions",
            haxis="Questions",
            vaxis="Number of correct answers"
        )
        context['irat_data'] = None
        context['grat_data'] = None

        return context

    def get_options(self, title, haxis, vaxis):
        """
        Get the specific options
        """

        options = {
            "title": _(title),
            "hAxis": _(haxis),
            "vAxis": _(vaxis)
        }

        return options

    def get_object(self, queryset=None):
        """
        Get gamification students points
        """

        graphic = []

        questions = Question.objects.filter(session=self.get_session(), is_exercise=False)

        count = 0
        for question in questions:
            report = []
            count += 1
            report.append("Q{0}".format(count))

            iRAT_submissions = IRATSubmission.objects.filter(session=self.get_session(), question=question)
            report.append(self.get_total_score(iRAT_submissions))

            gRAT_submissions = GRATSubmission.objects.filter(session=self.get_session(), question=question)
            report.append(self.get_total_score(gRAT_submissions))

            graphic.append(report)

        return graphic

    def get_total_score(self, submissions):
        """
        Get the total score of submission passed
        """

        discipline = self.get_discipline()

        total_score = 0
        for submission in submissions:
            if submission.user in discipline.students.all():
                total_score += submission.score

        return total_score