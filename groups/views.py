from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from core.generics import ObjectRedirectView
from .models import Group
from .forms import StudentGroupForm

# Get the custom user from settings
User = get_user_model()


class ListGroupView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to see all groups of discipline.
    """

    template_name = 'groups/list.html'
    paginate_by = 5
    context_object_name = 'groups'

    # Permissions
    permissions_required = [
        'show_discipline_groups_permission'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ListGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = StudentGroupForm()
        return context

    def get_queryset(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups


class CreateGroupView(LoginRequiredMixin,
                      PermissionMixin,
                      CreateView):
    """
    View to create a new group to discipline.
    """

    model = Group
    template_name = 'groups/list.html'
    form_class = StudentGroupForm

    # Permissions
    permissions_required = [
        'change_own_group'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Receive the form already validated to create a group.
        """

        form.instance.discipline = self.get_discipline()

        form.save()

        messages.success(self.request, _('Group created successfully.'))

        return super(CreateGroupView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to group list with error.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url


class UpdateGroupView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    View to update a specific group.
    """

    model = Group
    template_name = 'groups/form.html'
    context_object_name = 'group'
    form_class = StudentGroupForm

    # Permissions
    permissions_required = [
        'change_own_group'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside group template.
        """

        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('Group updated successfully.'))

        return super(UpdateGroupView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url


class DeleteGroupView(LoginRequiredMixin,
                      PermissionMixin,
                      DeleteView):
    """
    View to delete a specific group.
    """

    model = Group

    # Permissions
    permissions_required = [
        'change_own_group'
    ]

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        messages.success(self.request, _("Group deleted successfully."))

        return success_url


class ProvideGroupView(LoginRequiredMixin,
                       PermissionMixin,
                       ObjectRedirectView):
    """
    Make groups available for students.
    """

    template_name = 'groups/list.html'
    permissions_required = ['change_own_group']

    def get_object(self):
        """
        Get discipline by url slug.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_object()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        if discipline.was_group_provided:
            messages.success(self.request, _("Groups available."))
        else:
            messages.success(self.request, _("Groups unavailable."))

        return success_url

    def action(self, request, *args, **kwargs):
        """
        Change groups permission to available or unavailable.
        """

        discipline = self.get_object()

        if discipline.was_group_provided:
            discipline.was_group_provided = False
        else:
            discipline.was_group_provided = True

        discipline.save()

        return redirect(self.get_success_url())


class ListAvailableStudentsView(LoginRequiredMixin,
                                PermissionMixin,
                                ListView):
    """
    Show a list of students available to insert into groups.
    """

    template_name = 'groups/students.html'
    paginate_by = 12
    context_object_name = 'students'
    permissions_required = ['change_own_group']

    def get_discipline(self):
        """
        Get the specific discipline by url.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_group(self):
        """
        Get the specific group by url
        """

        group = get_object_or_404(
            Group,
            pk=self.kwargs.get('pk', '')
        )

        return group

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'groups:list',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_queryset(self):
        """
        List all available students to insert into discipline.
        """

        self.discipline = self.get_discipline()
        students = self.discipline.students.all()

        students_available = []

        for student in students:
            available = self.is_available(student)

            if available is True:
                students_available.append(student)

        return students_available

    def is_available(self, student):
        """
        Scroll through the discipline groups and return True if it is not
        in any group.
        """

        available = False

        for group in self.discipline.groups.all():
            if student in group.students.all():
                available = False
                break
            else:
                available = True

        return available

    def get_context_data(self, **kwargs):
        """
        Insert discipline and group instance into student list.
        """

        context = super(ListAvailableStudentsView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['group'] = self.get_group()
        return context


class InsertStudentView(LoginRequiredMixin,
                        PermissionMixin,
                        ObjectRedirectView):
    """
    Insert a student inside group.
    """

    template_name = 'groups/students.html'
    permissions_required = ['change_own_group']

    def get_discipline(self):
        """
        Get the specific discipline by url.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_group(self):
        """
        Get the specific group by url
        """

        group = get_object_or_404(
            Group,
            pk=self.kwargs.get('group_id', '')
        )

        return group

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'groups:list',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url

    def action(self, request, *args, **kwargs):
        """
        Insert a student into the group action.
        and redirect to success url
        """

        student = get_object_or_404(
            User,
            pk=self.kwargs.get('student_id', '')
        )

        self.insert(student)

        return redirect(self.get_success_url())

    def insert(self, student):
        """
        Insert student into group.
        """

        group = self.get_group()

        if group.students.count() >= group.students_limit:

            messages.error(
                self.request,
                _("Crowded group.")
            )

        else:

            group.students.add(student)

            messages.success(
                self.request,
                _("{0} was inserted into the group: {1}"
                  .format(student.get_short_name(), group.title))
            )


class RemoveStudentView(LoginRequiredMixin,
                        PermissionMixin,
                        DeleteView):
    """
    Remove student from groups.
    """

    template_name = 'groups/students.html'
    permissions_required = ['change_own_group']

    def get_discipline(self):
        """
        Get the specific discipline by url.
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_group(self):
        """
        Get the specific group by url
        """

        group = get_object_or_404(
            Group,
            pk=self.kwargs.get('group_id', '')
        )

        return group

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'groups:list',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_success_url(self):
        """
        Create a success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'groups:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url

    def delete(self, request, *args, **kwargs):
        """
        Redirect to success url after remove the specific student
        from group.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('student_id', '')
        )

        self.remove_from_group(user)

        return redirect(self.get_success_url())

    def remove_from_group(self, student):
        """
        Remove specific student from group.
        """

        group = self.get_group()

        group.students.remove(student)

        messages.success(
            self.request,
            _("The student {0} was removed from {1}"
              .format(student.get_short_name(), group.title))
        )
