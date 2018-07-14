from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from core.permissions import PermissionMixin
from disciplines.models import Discipline

# Get the custom user from settings
User = get_user_model()


class UsersListView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    List of all user to insert into discipline, can search user by name,
    username, or email
    """

    template_name = 'students/users.html'
    context_object_name = 'users'
    ordering = 'name'
    paginate_by = 12
    permissions_required = [
        'change_own_discipline'
    ]

    def get_context_data(self, **kwargs):
        """
        Insert form into list view.
        """

        context = super(UsersListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def get_discipline(self):
        """
        Get the specific discipline.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_queryset(self, **kwargs):
        """
        Insert only available users, can't insert discipline teacher and users
        that are inside the discipline.
        """

        discipline = self.get_discipline()
        queryset = []

        users = User.objects.all()

        students = []
        for student in discipline.students.all():
            students.append(student)

        for monitor in discipline.monitors.all():
            students.append(monitor)

        for user in users:
            if user not in students and user != discipline.teacher:
                queryset.append(user)

        queryset = self.search(queryset)

        return queryset

    def search(self, users):
        """
        Search a specific user to insert into the discipline.
        """

        # From url after search get the ?q_info=...
        query = self.request.GET.get("q_info")
        if query:
            users = User.objects.filter(
                Q(name__icontains=query) |
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )

        return users
