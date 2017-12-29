from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from .models import DisciplineFile
from .forms import FileForm


class ListDisciplineFileView(LoginRequiredMixin,
                             PermissionMixin,
                             ListView):
    """
    View to see all file of discipline.
    """

    template_name = 'files/list.html'
    paginate_by = 10
    context_object_name = 'files'

    permissions_required = [
        'show_files_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the file belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into file context data.
        """

        context = super(ListDisciplineFileView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = FileForm()
        return context

    def get_queryset(self):
        """
        Get the files queryset from model database.
        """

        discipline = self.get_discipline()

        files = DisciplineFile.objects.filter(discipline=discipline)

        return files


class CreateDisciplineFileView(LoginRequiredMixin,
                               PermissionMixin,
                               CreateView):
    """
    View to insert a new file into the discipline.
    """

    model = DisciplineFile
    template_name = 'files/list.html'
    form_class = FileForm

    permissions_required = [
        'monitor_can_change'
    ]

    def get_discipline(self):
        """
        Take the discipline that the file belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Receive the form already validated to create a file.
        """

        form.instance.discipline = self.get_discipline()
        form.save()

        messages.success(self.request, _('File created successfully.'))

        return super(CreateDisciplineFileView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to form with form error.
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
            'files:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url


class EditDisciplineFileView(LoginRequiredMixin,
                             PermissionMixin,
                             UpdateView):
    """
    View to update a specific file.
    """

    model = DisciplineFile
    template_name = 'files/form.html'
    context_object_name = 'file'
    form_class = FileForm

    permissions_required = [
        'monitor_can_change'
    ]

    def get_discipline(self):
        """
        Take the discipline that the file belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside file form.
        """

        context = super(EditDisciplineFileView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('File updated successfully.'))

        return super(EditDisciplineFileView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'files:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url


class DeleteDisciplineFileView(LoginRequiredMixin,
                               PermissionMixin,
                               DeleteView):
    """
    View to delete a specific file.
    """

    model = DisciplineFile

    permissions_required = [
        'monitor_can_change'
    ]

    def get_discipline(self):
        """
        Take the discipline that the file belongs to
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
            'files:list',
            kwargs={'slug': discipline.slug}
        )

        messages.success(self.request, _("File deleted successfully."))

        return success_url
