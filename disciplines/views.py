"""
The list of user disciplines is in accounts.views.ProfileView
Disciplines functionalities
"""

# Django app
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView,
    ListView, FormView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q

# Core app
from core.permissions import ModelPermissionMixin, PermissionMixin
from core.generics import ObjectRedirectView
from core.utils import order

# Discipline app
from .forms import DisciplineForm, DisciplineEditForm, EnterDisciplineForm
from .models import Discipline
from rankingGroup.models import Ranking

# Get the custom user from settings
User = get_user_model()


class CreateDisciplineView(LoginRequiredMixin,
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
        Receive the form already validated to create a discipline.
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
        return super(CreateDisciplineView, self).form_valid(form)


class UpdateDisciplineView(LoginRequiredMixin,
                           PermissionMixin,
                           UpdateView):
    """
    View to update a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    form_class = DisciplineEditForm
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

        discipline = Discipline.objects.get(slug=self.kwargs.get('slug', ''))

        modify_student_limit = (
            discipline.students_limit < form.instance.students_limit
        )

        if modify_student_limit and discipline.is_closed:
            form.instance.is_closed = False

        form.save()

        messages.success(self.request, _("Discipline updated successfully."))

        # Redirect to success_url.
        return super(UpdateDisciplineView, self).form_valid(form)


class DeleteDisciplineView(LoginRequiredMixin,
                           PermissionMixin,
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
        return super(DeleteDisciplineView, self).get_success_url()


class ListDisciplineView(LoginRequiredMixin, ListView):
    """
    View to search a discipline and enter it.
    """

    template_name = 'disciplines/list.html'
    paginate_by = 10
    context_object_name = 'disciplines'

    def get_context_data(self, **kwargs):
        """
        Insert a form inside discipline list.
        """

        context = super(ListDisciplineView, self).get_context_data(**kwargs)
        context['form'] = EnterDisciplineForm()
        return context

    def get_queryset(self):
        """
        Get the discipline queryset from model database.
        """

        user = self.request.user

        # Disciplines available for user
        queryset = Discipline.objects.available(user)

        queryset = order(self, queryset)

        queryset = self.search_disciplines(queryset)

        return queryset

    def search_disciplines(self, disciplines):
        """
        Search from disciplines a specific discipline.
        """

        # From url after search get the ?q_info=...
        query = self.request.GET.get("q_info")
        if query:
            disciplines = Discipline.objects.search(query)

        return disciplines


class EnterDisciplineView(LoginRequiredMixin, FormView):
    """
    Insert students or monitors inside discipline.
    """

    form_class = EnterDisciplineForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'disciplines/list.html'

    def form_valid(self, form):
        """
        Form to insert students and monitors in the discipline.
        """

        success = self.enter_discipline(form)

        if success:
            # Redirect to success_url
            return super(EnterDisciplineView, self).form_valid(form)

        # Redirect to same page with error.
        redirect_url = reverse_lazy('disciplines:search')

        return redirect(redirect_url)

    def enter_discipline(self, form):
        """
        Verify if the password is correct and insert user in the discipline.
        """

        try:
            discipline = Discipline.objects.get(
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
                _("You have entered the discipline: {0}"
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
                _("There are no more monitor vacancies")
            )

            return False

        if self.request.user.id == discipline.teacher.id:
            messages.error(
                self.request,
                _("You can't get into your own discipline.")
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


class ShowDisciplineView(LoginRequiredMixin,
                         PermissionMixin,
                         DetailView):
    """
    View to show a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/details.html'
    permissions_required = [
        'show_ranking_permission'
    ]

    def get_context_data(self, **kwargs):
        """
        """
        discipline = self.get_object()

        context = super(ShowDisciplineView, self).get_context_data(**kwargs)
        context['ranking'] = self.get_ranking()

        return context


    def get_ranking(self):

        discipline = self.get_object()

        ranking = Ranking()
        try:
            ranking = Ranking.objects.get(discipline=discipline)
        except Ranking.DoesNotExist:
            ranking = None

        return ranking


class CloseDisciplineView(LoginRequiredMixin,
                          PermissionMixin,
                          DeleteView):

    model = Discipline
    template_name = 'disciplines/details.html'
    permissions_required = [
        'show_discipline_permission',
        'change_own_discipline'
    ]


    def delete(self, request, *args, **kwargs):
        """
        Close or open discipline.
        """



        discipline = self.get_object()

        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': discipline.slug},

        )

        if discipline.is_closed:
            #salva em lista os primeiros colocados - estatico
            #retira alunos e monitores
            discipline.is_closed = False
        else:
            discipline.is_closed = True

        discipline.save()

        # Show message for discipline status
        if discipline.is_closed:
            success_message = "Discipline was closed successfully."
            messages.success(self.request, success_message)
        else:
            success_message = "Discipline was open successfully."
            messages.success(self.request, success_message)

        return redirect(redirect_url)


class StudentListView(LoginRequiredMixin,
                      PermissionMixin,
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


class RemoveStudentView(LoginRequiredMixin,
                        PermissionMixin,
                        DeleteView):
    """
    Remove student from discipline.
    """

    template_name = 'disciplines/students.html'
    permissions_required = [
        'show_discipline_permission'
    ]

    def get_object(self):
        """
        Get discipline by url slug
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def delete(self, request, *args, **kwargs):
        """
        Redirect to success url after remove the specific student
        from discipline.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk', '')
        )

        discipline = self.get_object()

        is_logged_user = (self.request.user.id == user.id)
        is_teacher = (self.request.user.id == discipline.teacher.id)

        if is_logged_user or is_teacher:
            success_url = self.remove_from_discipline(user, is_teacher)
            return redirect(success_url)

        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': discipline.slug}
        )

        messages.error(
            self.request,
            _("You can't remove {0} from {1}"
              .format(user.get_short_name(), discipline.title))
        )

        return redirect(redirect_url)

    def remove_from_discipline(self, user, is_teacher=True):
        """
        Remove user from discipline.
        """

        discipline = self.get_object()

        if user in discipline.students.all():
            discipline.students.remove(user)

            if discipline.is_closed:
                discipline.is_closed = False
                discipline.save()
        else:
            discipline.monitors.remove(user)

        if is_teacher:
            messages.success(
                self.request,
                _("You have removed {0} from {1}"
                  .format(user.get_short_name(), discipline.title))
            )

            success_url = reverse_lazy(
                'disciplines:students',
                kwargs={'slug': discipline.slug}
            )
        else:
            messages.success(
                self.request,
                _("You left the discipline {0}"
                  .format(discipline.title))
            )

            success_url = reverse_lazy('accounts:profile')

        return success_url


class ListUsersView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    List of all user to insert into discipline, can search user by name,
    username, or email
    """

    template_name = 'disciplines/users.html'
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

        context = super(ListUsersView, self).get_context_data(**kwargs)
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


class InsertStudentView(LoginRequiredMixin,
                        PermissionMixin,
                        ObjectRedirectView):
    """
    Insert a student or monitor inside discipline by teacher.
    """

    template_name = 'disciplines/users.html'
    permissions_required = [
        'change_own_discipline'
    ]

    def get_object(self):
        """
        Get discipline by url slug
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_object()

        success_url = reverse_lazy(
            'disciplines:users',
            kwargs={'slug': discipline.slug}
        )

        return success_url

    def action(self, request, *args, **kwargs):
        """
        Insert a user into discipline.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk', '')
        )

        discipline = self.get_object()

        if user.is_teacher:
            success = self.insert_monitor(user, discipline)
        else:
            success = self.insert_student(user, discipline)

        if success:
            messages.success(
                self.request,
                _("{0} was inserted in the discipline: {1}"
                  .format(user.get_short_name(), discipline.title))
            )

        return redirect(self.get_success_url())

    def insert_monitor(self, user, discipline):
        """
        If user is a teacher, he will have all permission of monitor
        If monitor number is bigger than monitors limit, can't enter.
        """

        if discipline.monitors.count() >= discipline.monitors_limit:
            messages.error(
                self.request,
                _("There are no more monitor vacancies")
            )

            return False

        if user == discipline.teacher:
            messages.error(
                self.request,
                _("You can't get into your own discipline.")
            )

            return False

        discipline.monitors.add(user)

        return True

    def insert_student(self, user, discipline):
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

        discipline.students.add(user)

        return True


class ChangeStudentView(LoginRequiredMixin,
                        PermissionMixin,
                        ObjectRedirectView):
    """
    Change student to monitor or monitor to student if the monitor is no a
    teacher.
    """

    template_name = 'disciplines/students.html'
    permissions_required = [
        'change_own_discipline'
    ]

    def get_object(self):
        """
        Get discipline by url slug
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_object()

        success_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': discipline.slug}
        )

        return success_url

    def action(self, request, *args, **kwargs):
        """
        Insert a user into discipline.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk', '')
        )

        discipline = self.get_object()

        success = self.change_user(user, discipline)

        if success:
            messages.success(self.request, _("Successful modification"))

        return redirect(self.get_success_url())

    def change_user(self, user, discipline):
        """
        Change user to monitor or student.
        """

        if user.is_teacher:
            messages.error(
                self.request,
                _("You can't turn a teacher into a student.")
            )

            return False

        if user in discipline.students.all():
            exceeded = self.monitor_limit_exceeded(discipline)

            if not exceeded:
                discipline.students.remove(user)
                discipline.monitors.add(user)
            else:
                return False
        else:
            exceeded = self.student_limit_exceeded(discipline)

            if not exceeded:
                discipline.monitors.remove(user)
                discipline.students.add(user)
            else:
                return False

        return True

    def student_limit_exceeded(self, discipline):
        """
        Verify if student limit exceeded.
        """

        if discipline.students.count() >= discipline.students_limit:

            messages.error(
                self.request,
                _("Student limit exceeded.")
            )

            return True

        return False

    def monitor_limit_exceeded(self, discipline):
        """
        Verify if monitor limit exceeded.
        """

        if discipline.monitors.count() >= discipline.monitors_limit:

            messages.error(
                self.request,
                _("Monitor limit exceeded.")
            )

            return True

        return False
