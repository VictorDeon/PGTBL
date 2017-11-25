"""
The list of user disciplines is in accounts.views.ProfileView
Disciplines functionalities
"""

# Django app
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView
)

# Core app
from core.permissions import ModelPermissionMixin, ObjectPermissionMixin
from core.generics import FormListView, FormDetailView
from core.utils import order

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
        # Save the instance to slugify
        form.save()

        # Autocomplete slug url with id-title-classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        # Save slug
        form.save()

        messages.success(self.request, _('Discipline created successfully.'))

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

        # Autocomplete slug url with id-title-classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        form.save()

        messages.success(self.request, _("Discipline updated successfully."))

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

        queryset = order(self, queryset)
        queryset = self.search_disciplines(queryset)

        return queryset

    def form_valid(self, form):
        """
        Form to insert students and monitors in the discipline.
        """

        success = self.enter_discipline(form)

        if success:
            # Redirect to success_url
            return super(DisciplineListSearchView, self).form_valid(form)

        # Redirect to same page with error.
        return super(DisciplineListSearchView, self).form_invalid(form)

    def enter_discipline(self, form):
        """
        Verify if the password is correct and insert user in the discipline.
        """

        queryset = self.get_queryset()

        try:
            discipline = queryset.get(
                Q(password=form.cleaned_data['password']),
                Q(slug=self.kwargs.get('slug', ''))
            )
        except Exception:
            messages.error(
                self.request,
                _("Incorrect Password.")
            )

            return False

        if discipline.is_closed:
            messages.error(
                self.request,
                _("Discipline is closed.")
            )

            return False

        if self.request.user.is_teacher:
            success = self.insert_monitor(discipline)
        else:
            success = self.insert_student(discipline)

        if success:
            messages.success(
                self.request,
                _("You have been entered into the discipline: {0}"
                  .format(discipline.title))
            )

            return True

        return False

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

            return False

        discipline.monitors.add(self.request.user)

        return True

    def insert_student(self, discipline):
        """
        If user is a student, he will have all permission of student
        If students number is bigger than student limit of discipline, close it
        """

        if discipline.students.count() >= discipline.students_limit:
            if not discipline.is_closed:
                discipline.is_closed = True
                discipline.save()

            messages.error(
                self.request,
                _("Crowded discipline.")
            )

            return False

        discipline.students.add(self.request.user)

        return True

    def search_disciplines(self, disciplines):
        """
        Search from disciplines a specific discipline.
        """

        # From url after search get the ?q_info=...
        query = self.request.GET.get("q_info")
        if query:
            disciplines = Discipline.objects.search(query)

        return disciplines


class ShowDisciplineView(LoginRequiredMixin,
                         ObjectPermissionMixin,
                         FormDetailView):
    """
    View to show a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/details.html'
    permissions_required = [
        'show_discipline_permission'
    ]

    def get_success_url(self):
        """
        Close or open discipline.
        """

        discipline = self.get_object()

        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': discipline.slug}
        )

        if discipline.is_closed:
            discipline.is_closed = False
        else:
            discipline.is_closed = True

        discipline.save()

        return redirect_url


class StudentListView(LoginRequiredMixin,
                      ObjectPermissionMixin,
                      ListView):
    """
    Insert, delete and list all students from specific discipline.
    """

    template_name = 'disciplines/students.html'
    paginate_by = 12
    context_object_name = 'students'
    permissions_required = [
        'show_discipline_students_permission'
    ]

    def get_queryset(self):
        """
        List all students and monitors from discipline.
        """

        self.discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        # Insert monitors and students into one queryset
        queryset = (self.discipline.students.all() |
                    self.discipline.monitors.all())

        students = self.students_filter(queryset)

        return students

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

        filtered = self.request.GET.get('order')
        if filtered == 'students':
            queryset = self.discipline.students.all()
        elif filtered == 'monitors':
            queryset = self.discipline.monitors.all()

        return queryset


class RemoveStudentView(LoginRequiredMixin,
                        ObjectPermissionMixin,
                        FormDetailView):
    """
    Remove student from discipline.
    """

    template_name = 'disciplines/students.html'
    permissions_required = [
        'show_discipline_students_permission'
    ]

    def get_queryset(self):
        """
        List all students and monitors from discipline.
        """

        self.discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        # Insert monitors and students into one queryset
        students = (self.discipline.students.all() |
                    self.discipline.monitors.all())

        return students

    def get_success_url(self):
        """
        Redirect to success url after remove the specific student
        from discipline.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk', '')
        )

        is_logged_user = (self.request.user.id == user.id)
        is_teacher = (self.request.user.id == self.discipline.teacher.id)

        if is_logged_user or is_teacher:
            success_url = self.remove_from_discipline(user, is_teacher)
            return success_url

        messages.error(
            self.request,
            _("You can't remove {0} from {1}"
              .format(user.get_short_name(), self.discipline.title))
        )

        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )

        return redirect_url

    def remove_from_discipline(self, user, is_teacher=True):
        """
        Remove user from discipline.
        """

        if user in self.discipline.students.all():
            self.discipline.students.remove(user)
        else:
            self.discipline.monitors.remove(user)

        if is_teacher:
            messages.success(
                self.request,
                _("You have removed {0} from {1}"
                  .format(user.get_short_name(), self.discipline.title))
            )

            success_url = reverse_lazy(
                'disciplines:students',
                kwargs={'slug': self.discipline.slug}
            )
        else:
            messages.success(
                self.request,
                _("You left the discipline {0}"
                  .format(self.discipline.title))
            )

            success_url = reverse_lazy('accounts:profile')

        return success_url
