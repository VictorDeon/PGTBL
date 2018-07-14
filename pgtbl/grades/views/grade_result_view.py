from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grades.models import FinalGrade


class GradeResultView(LoginRequiredMixin,
                      PermissionMixin,
                      ListView):
    """
    Show the list of students with their final grade.
    """

    template_name = 'grades/result.html'
    context_object_name = 'grades'

    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into session context data.
        """

        context = super(GradeResultView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def get_queryset(self):
        """
        Get the tbl sessions queryset from model database.
        """

        grades = []
        discipline = self.get_discipline()

        for student in discipline.students.all():
            grade, created = FinalGrade.objects.get_or_create(
                discipline=discipline,
                student=student
            )
            grades.append(grade)

        return grades
