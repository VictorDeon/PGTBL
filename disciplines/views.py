"""
The list of user disciplines is in accounts.views.ProfileView
Disciplines functionalities
"""

# Django app
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.views.generic import (
    CreateView, UpdateView, DeleteView
)
from django.db.models import Q

# Core app
from core.mixins import PermissionRequiredMixin, FormListView

# Discipline app
from .forms import DisciplineForm, EnterDisciplineForm
from .models import Discipline

# Get the custom user from settings
User = get_user_model()


class DisciplineCreationView(LoginRequiredMixin,
                             PermissionRequiredMixin,
                             CreateView):
    """
    View to create a new discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    form_class = DisciplineForm
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    user_check_failure_path = reverse_lazy('accounts:profile')
    permission_required = 'disciplines.add_discipline'

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # Specifies who is the creator of the discipline
        form.instance.teacher = self.request.user

        form.save()

        # Autocomplete slug with id - title - classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        # Return to form_valid function from django to finish creation.
        return super(DisciplineCreationView, self).form_valid(form)


class DisciplineUpdateView(LoginRequiredMixin,
                           PermissionRequiredMixin,
                           UpdateView):
    """
    View to update a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    slug_url_kwargs = 'slug'

    # Form
    fields = [
        'title', 'course', 'description', 'classroom',
        'password', 'students_limit', 'monitors_limit'
    ]
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    user_check_failure_path = reverse_lazy('accounts:profile')
    permission_required = 'disciplines.change_discipline'


class DisciplineDeleteView(LoginRequiredMixin,
                           PermissionRequiredMixin,
                           DeleteView):
    """
    View to delete a specific discipline.
    """

    model = Discipline
    success_url = reverse_lazy('accounts:profile')
    slug_url_kwargs = 'slug'

    # Permissions
    user_check_failure_path = reverse_lazy('accounts:profile')
    permission_required = 'disciplines.change_discipline'


class DisciplineListSearchView(LoginRequiredMixin, FormListView):
    """
    View to search a discipline and enter it.
    """

    template_name = 'disciplines/list.html'
    paginate_by = 10
    context_object_name = 'disciplines'

    # Form
    form_class = EnterDisciplineForm
    success_url = reverse_lazy('accounts:profile')

    def get_queryset(self):
        """
        Get the specific queryset from model database.
        """

        user = self.request.user

        # Remove from queryset the discipline teacher, students and monitors
        # that are inside discipline and disciplines that are closed.
        queryset = Discipline.objects.exclude(
            Q(teacher=user) |
            Q(students__email=user.email) |
            Q(monitors__email=user.email) |
            Q(is_closed=True)
        ).distinct()

        queryset = self.order_disciplines(queryset)
        queryset = self.search_disciplines(queryset)
        return queryset

    def form_valid(self, form):
        """
        Form to insert students and monitors in the discipline.
        """

        password = form.cleaned_data['password']

        self.enter_discipline(password)

        # Save form and redirect to success_url
        return super(DisciplineListSearchView, self).form_valid(form)

    def enter_discipline(self, password):
        """
        Verify if the password is correct and insert user in the discipline.
        """

        queryset = self.get_queryset()
        disciplines = queryset.filter(password=password)
        slug = self.kwargs.get('slug', '')

        for discipline in disciplines:
            if discipline.slug == slug:
                self.insert_user(discipline)
            else:
                print("Disciplina não encontrada - mensagem de erro!")

    def insert_user(self, discipline):
        """
        Insert user in the discipline and change his permissions.
        If user is a teacher, he will have all permission of monitor
        If user is a student, he will have all permission of student
        If students number if bigger than student limit of discipline, close it
        """

        user = self.request.user

        if user.is_teacher:
            if discipline.monitors.count() >= discipline.monitors_limit:
                print("Não há mais vagas para monitor - Mensagem de erro.")
            else:
                discipline.monitors.add(user)
                group = get_object_or_404(Group, name='Monitor')
                group.user_set.add(user)
        else:
            if discipline.students.count() >= discipline.students_limit:
                print("Disciplina lotada. - Mensagem de erro.")
                discipline.is_closed = True
            else:
                discipline.students.add(user)

    def search_disciplines(self, disciplines):
        """
        Search from disciplines a specific discipline.
        """

        query = self.request.GET.get("q_info")
        if query:
            # Verify if discipline title, description, course and classroom
            # contains the query specify by user and filter all disciplines
            # that satisfies this query.
            disciplines = disciplines.filter(
                              Q(title__icontains=query) |
                              Q(description__icontains=query) |
                              Q(course__icontains=query) |
                              Q(classroom__icontains=query) |
                              Q(teacher__name__icontains=query)
                          ).distinct()

        return disciplines

    def order_disciplines(self, disciplines):
        """
        Order disciplines by title, couse, or classroom
        """

        # Get the filter by key argument from url
        ordered = self.request.GET.get('order')
        if ordered:
            disciplines = disciplines.order_by(ordered)

        return disciplines
