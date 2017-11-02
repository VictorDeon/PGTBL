"""
The list of user disciplines is in accounts.views.ProfileView
Disciplines functionalities
"""

# Django app
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.contrib import messages

# Core app
from core.permissions import ModelPermissionMixin, ObjectPermissionMixin
from core.generics import FormListView

# Discipline app
from .forms import DisciplineForm, EnterDisciplineForm
from .models import Discipline

# Get the custom user from settings
User = get_user_model()


class DisciplineCreationView(LoginRequiredMixin,
                             ModelPermissionMixin,
                             CreateView):
    """
    View to create a new discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    form_class = DisciplineForm
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    failure_redirect_path = reverse_lazy('accounts:profile')
    permissions_required = [
        'create_discipline'
    ]

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # Specifies who is the creator of the discipline
        form.instance.teacher = self.request.user
        form.save()

        messages.success(self.request, _('Discipline created successfully.'))

        # Autocomplete slug url with id-title-classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        # Redirect to success url
        return super(DisciplineCreationView, self).form_valid(form)


class DisciplineUpdateView(LoginRequiredMixin,
                           ObjectPermissionMixin,
                           UpdateView):
    """
    View to update a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'

    # Form
    fields = [
        'title', 'course', 'description', 'classroom',
        'password', 'students_limit', 'monitors_limit'
    ]
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    failure_redirect_path = reverse_lazy('accounts:profile')
    permissions_required = [
        'change_own_discipline'
    ]

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        messages.success(self.request, _("Discipline updated successfully."))

        # Autocomplete slug url with id-title-classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        # Redirect to success_url.
        return super(DisciplineUpdateView, self).form_valid(form)


class DisciplineDeleteView(LoginRequiredMixin,
                           ObjectPermissionMixin,
                           DeleteView):
    """
    View to delete a specific discipline.
    """

    model = Discipline
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    failure_redirect_path = reverse_lazy('accounts:profile')
    permissions_required = [
        'change_own_discipline'
    ]

    def get_success_url(self):
        """
        Redirect to success_url and show a message.
        """

        messages.success(self.request, _("Discipline deleted successfully."))

        # Redirect to success_url
        return super(DisciplineDeleteView, self).get_success_url()


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

        # Disciplines available for user
        queryset = Discipline.objects.available(user)

        queryset = self.order_disciplines(queryset)
        queryset = self.search_disciplines(queryset)

        return queryset

    def form_valid(self, form):
        """
        Form to insert students and monitors in the discipline.
        """

        # Field of form.
        password = form.cleaned_data['password']

        success = self.enter_discipline(password)

        if success:
            # Redirect to success_url
            return super(DisciplineListSearchView, self).form_valid(form)
        else:
            # Redirect to same page with error.
            return redirect('disciplines:search')

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

                messages.success(
                    self.request,
                    _("You have been entered into the discipline: {0}"
                      .format(discipline))
                )

                return True

        messages.error(
            self.request,
            _("Incorrect Password.")
        )

        return False

    def insert_user(self, discipline):
        """
        Insert user in the discipline and change his permissions.
        """

        if self.request.user.is_teacher:
            self.insert_monitor(discipline)
        else:
            self.insert_student(discipline)

    def insert_monitor(self, discipline):
        """
        If user is a teacher, he will have all permission of monitor
        If monitor number is bigger than monitors limit, can't enter.
        """

        if discipline.monitors.count() >= discipline.monitors_limit:
            messages.error(
                self.request,
                _("There are no more vacancies to monitor")
            )
        else:
            discipline.monitors.add(self.request.user)
            group = get_object_or_404(Group, name='Monitor')
            group.user_set.add(self.request.user)

    def insert_student(self, discipline):
        """
        If user is a student, he will have all permission of student
        If students number is bigger than student limit of discipline, close it
        """

        if discipline.students.count() >= discipline.students_limit:
            messages.error(
                self.request,
                _("Crowded discipline.")
            )
            discipline.is_closed = True
        else:
            discipline.students.add(self.request.user)

    def search_disciplines(self, disciplines):
        """
        Search from disciplines a specific discipline.
        """

        # From url after search get the ?q_info=...
        query = self.request.GET.get("q_info")
        if query:
            disciplines = Discipline.objects.search(query)

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
