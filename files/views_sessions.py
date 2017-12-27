from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView
)
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from .models import SessionFile
from .forms import SessionFileForm


class ListSessionFileView(LoginRequiredMixin,
                          PermissionMixin,
                          ListView):
    """
    View to see all tbl session file of discipline.
    """

    template_name = 'files/session_list.html'
    paginate_by = 10
    context_object_name = 'files'

    # Modificar
    permissions_required = [
        'show_files_permission',
        'show_tbl_file_session'
    ]

    def get_discipline(self):
        """
        Take the discipline that the file belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the file belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into file context data.
        """

        context = super(ListSessionFileView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['form'] = SessionFileForm()
        return context

    def get_queryset(self):
        """
        Get the files queryset from model database.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        # Modificar
        files = SessionFile.objects.filter(
            discipline=discipline,
            session=session
        )

        return files


class CreateSessionFileView(LoginRequiredMixin,
                            PermissionMixin,
                            CreateView):
    """
    View to insert a new file into the tbl session.
    """

    model = SessionFile
    template_name = 'files/session-list.html'
    form_class = SessionFileForm

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

    def get_session(self):
        """
        Take the session that the file belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def form_valid(self, form):
        """
        Receive the form already validated to create a file.
        """

        form.instance.discipline = self.get_discipline()
        form.instance.session = self.get_session()
        form.save()

        messages.success(self.request, _('File created successfully.'))

        return super(CreateSessionFileView, self).form_valid(form)

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
        session = self.get_session()

        success_url = reverse_lazy(
            'files:session-list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url


class EditSessionFileView(LoginRequiredMixin,
                          PermissionMixin,
                          UpdateView):
    """
    View to update a specific session file.
    """

    model = SessionFile
    template_name = 'files/session_form.html'
    context_object_name = 'file'
    form_class = SessionFileForm

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

    def get_session(self):
        """
        Take the session that the file belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Get the specific file from tbl session of discipline.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        archive = SessionFile.objects.get(
            discipline=discipline,
            session=session,
            pk=self.kwargs.get('file_id', '')
        )

        return archive

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside file form.
        """

        context = super(EditSessionFileView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('File updated successfully.'))

        return super(EditSessionFileView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'files:session-list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url


class DeleteSessionFileView(LoginRequiredMixin,
                            PermissionMixin,
                            DeleteView):
    """
    View to delete a specific tbl session file.
    """

    model = SessionFile

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

    def get_session(self):
        """
        Take the session that the file belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Get the specific file from tbl session of discipline.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        archive = SessionFile.objects.get(
            discipline=discipline,
            session=session,
            pk=self.kwargs.get('file_id', '')
        )

        return archive

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'files:session-list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        messages.success(self.request, _("File deleted successfully."))

        return success_url
