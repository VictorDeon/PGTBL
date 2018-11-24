from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grades.models import Grade
from grat.models import GRATSubmission
from groups.models import Group
from irat.models import IRATSubmission
from modules.models import TBLSession
from modules.utils import get_datetimes
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
        context['questions_options'] = {
            "title": _("Number of correct answers for questions"),
            "hAxis": _("Questions"),
            "vAxis": _("Number of correct answers")
        }
        context['questions'] = self.get_questions()
        context['irat_data'] = self.get_irat_data()
        context['grat_data'] = self.get_grat_data()
        context['irat_average'] = self.get_irat_average()
        context['grat_average'] = self.get_grat_average()

        return context

    def get_questions(self):
        """
        Get the question to iRAT and gRAT tests.
        """

        questions = Question.objects.filter(session=self.get_session(), is_exercise=False)

        return questions

    def get_object(self, queryset=None):
        """
        Get gamification students points
        """

        graphic = []

        questions = self.get_questions()

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

    def get_irat_data(self):
        """
        Get the iRAT data to populate graphic.
        """

        questions = self.get_questions()

        discipline = self.get_discipline()

        result = []
        for student in discipline.students.all():
            table = [student.username]

            for question in questions:
                try:
                    submission = IRATSubmission.objects.get(
                        session=self.get_session(),
                        question=question,
                        user=student
                    )
                    table.append(submission.score)
                except:
                    table.append(0)

            result.append(table)

        return result

    def get_irat_average(self):
        """
        Get the iRAT average
        """

        grades = Grade.objects.filter(
            session=self.get_session()
        )

        total = 0
        for grade in grades:
            total += grade.irat

        if len(grades) > 0:
            average = total/len(grades)
        else:
            average = 0

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        result = {
            'average': average,
            'data': irat_datetime
        }

        return result

    def get_grat_average(self):
        """
        Get the iRAT average
        """

        grades = Grade.objects.filter(
            session=self.get_session()
        )

        total = 0
        for grade in grades:
            total += grade.grat

        if len(grades) > 0:
            average = total / len(grades)
        else:
            average = 0

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        result = {
            'average': average,
            'data': grat_datetime
        }

        return result

    def get_grat_data(self):
        """
        Get the gRAT data to populate graphic.
        """

        questions = self.get_questions()

        groups = Group.objects.filter(discipline=self.get_discipline())

        result = []
        for group in groups:
            table = []
            table.append(group.title)

            for question in questions:
                try:
                    submission = GRATSubmission.objects.get(
                        session=self.get_session(),
                        question=question,
                        group=group
                    )
                    table.append(submission.score)
                except:
                    table.append(0)

            result.append(table)

        return result