from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline


class StudentListView(LoginRequiredMixin,
                      PermissionMixin,
                      ListView):
    """
    Insert, delete and list all students from specific discipline.
    """

    template_name = 'students/list.html'
    paginate_by = 12
    context_object_name = 'students'
    permissions_required = [
        'show_discipline_students_permission'
    ]

    def get_queryset(self):
        """
        List all students and monitors from discipline.
        """

        self.discipline = self.get_discipline()

        students = self.discipline.students.all()
        monitors = self.discipline.monitors.all()

        # Insert monitors and students into one queryset
        queryset = []
        for student in students:
            queryset.append(student)

        for monitor in monitors:
            queryset.append(monitor)

        queryset = self.students_filter(queryset)

        return queryset

    def get_discipline(self):
        """
        Get the specific discipline.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert discipline instance into student list.
        """

        context = super(StudentListView, self).get_context_data(**kwargs)
        context['discipline'] = self.discipline
        return context

    def students_filter(self, queryset):
        """
        Filter by monitor or students
        """

        filtered = self.request.GET.get('filter')
        if filtered == 'students':
            queryset = self.discipline.students.all()
        elif filtered == 'monitors':
            queryset = self.discipline.monitors.all()

        return queryset
