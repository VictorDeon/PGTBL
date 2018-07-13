# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# Application imoports
from disciplines.models import Discipline


class ProfileView(LoginRequiredMixin, ListView):
    """
    Class to read a profile user and his disciplines.
    """

    paginate_by = 6
    template_name = 'accounts/profile.html'
    context_object_name = 'disciplines'

    def get_queryset(self):
        """
        If user is a student get the disciplines that he is taking
        If user is a teacher get the created disciplines and disciplines
        that he is monitor
        """

        queryset = self.filter_student_disciplines()

        if self.request.user.is_teacher:
            queryset = self.filter_teacher_disciplines()

        return queryset

    def filter_teacher_disciplines(self):
        """
        Get disciplines that teacher created or is a monitor.
        """

        created_disciplines = Discipline.objects.filter(
            teacher=self.request.user
        )

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user
        )

        # Join the created disciplines list and monitor disciplines list
        queryset = []
        for discipline in created_disciplines:
            queryset.append(discipline)

        for discipline in monitor_disciplines:
            queryset.append(discipline)

        # Get the filter by key argument from url
        filtered = self.request.GET.get('filter')

        if filtered == 'created':
            queryset = created_disciplines
        elif filtered == 'monitor':
            queryset = monitor_disciplines

        return queryset

    def filter_student_disciplines(self):
        """
        Get the students disciplines that he is taking
        """

        student_disciplines = Discipline.objects.filter(
            students=self.request.user
        )

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user
        )

        queryset = []
        for discipline in student_disciplines:
            queryset.append(discipline)

        for discipline in monitor_disciplines:
            queryset.append(discipline)

        # Get the filter by key argument from url
        filtered = self.request.GET.get('filter')

        if filtered == 'student':
            queryset = student_disciplines
        elif filtered == 'monitor':
            queryset = monitor_disciplines

        return queryset
