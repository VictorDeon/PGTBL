from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView
)
from disciplines.models import Discipline
from .models import Group
from .forms import StudentGroupForm


class ListGroupView(LoginRequiredMixin, ListView):
    """
    View to see all groups of discipline.
    """

    template_name = 'groups/list.html'
    paginate_by = 5
    context_object_name = 'groups'

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


class CreateGroupView(LoginRequiredMixin, CreateView):
    """
    View to create a new group to discipline.
    """

    model = Group
    template_name = 'groups/list.html'
    form_class = StudentGroupForm

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


class UpdateGroupView(LoginRequiredMixin, UpdateView):
    """
    View to update a specific group.
    """

    model = Group
    template_name = 'groups/form.html'
    context_object_name = 'group'
    form_class = StudentGroupForm

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


class DeleteGroupView(LoginRequiredMixin, DeleteView):
    """
    View to delete a specific group.
    """

    model = Group

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

        messages.success(self.request, _("Discipline deleted successfully."))

        return success_url
