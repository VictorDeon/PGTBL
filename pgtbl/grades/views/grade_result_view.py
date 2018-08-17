from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grades.models import FinalGrade


class GradeResultView(LoginRequiredMixin, ListView):
    """
    Show the list of students with their final grade.
    """

    template_name = 'grades/result.html'
    context_object_name = 'grades'

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
            result, created = FinalGrade.objects.get_or_create(
                discipline=discipline,
                student=student
            )
            grade = result.calcule_final_grade()
            result.final_grade = grade

            if grade >= 5:
                result.status = _("Approved")
            else:
                result.status = _("Disapproved")

            result.save()

            grades.append(result)

        return grades
