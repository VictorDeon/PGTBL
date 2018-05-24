from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView,
    DetailView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from .models import TBLSession
from .utils import get_datetimes
from .forms import TBLSessionForm


class ListTBLSessionView(LoginRequiredMixin,
                         PermissionMixin,
                         ListView):
    """
    View to see all discipline tbl sessions.
    """

    template_name = 'TBLSessions/list.html'
    paginate_by = 5
    context_object_name = 'sessions'

    permissions_required = [
        'show_sessions_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into session context data.
        """

        context = super(ListTBLSessionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = TBLSessionForm()
        return context

    def get_queryset(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        sessions = TBLSession.objects.filter(discipline=discipline)

        return sessions


class CreateSessionView(LoginRequiredMixin,
                        PermissionMixin,
                        CreateView):
    """
    View to insert a new tbl session into the discipline.
    """

    model = TBLSession
    template_name = 'TBLSessions/list.html'
    form_class = TBLSessionForm

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Receive the form already validated to create a session.
        """

        form.instance.discipline = self.get_discipline()
        form.save()

        messages.success(self.request, _('TBL session created successfully.'))

        return super(CreateSessionView, self).form_valid(form)



    def form_invalid(self, form):
        """
        Redirect to form with form errors.
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
            'TBLSessions:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url


class EditSessionView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    View to update a specific tbl session.
    """

    model = TBLSession
    template_name = 'TBLSessions/form.html'
    context_object_name = 'session'
    form_class = TBLSessionForm

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside tbl session form template.
        """

        context = super(EditSessionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """
        messages.success(self.request, _('TBL session updated successfully.'))

        return super(EditSessionView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'TBLSessions:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url


class DeleteSessionView(LoginRequiredMixin,
                        PermissionMixin,
                        DeleteView):
    """
    View to delete a specific tbl session.
    """

    model = TBLSession

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
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
            'TBLSessions:list',
            kwargs={'slug': discipline.slug}
        )

        messages.success(self.request, _("TBL session deleted successfully."))

        return success_url

class CloseSessionView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    View to close a specific tbl session.
    """

    model = TBLSession
    template_name = 'TBLSessions/form.html'
    context_object_name = 'session'
    fields = ['is_closed']

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside tbl session form template.
        """

        context = super(CloseSessionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        self.object.is_closed = True
        messages.success(self.request, _('TBL session closed successfully.'))
        return super(CloseSessionView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'TBLSessions:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url

class OpenSessionView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    View to update a specific tbl session.
    """

    model = TBLSession
    template_name = 'TBLSessions/form.html'
    context_object_name = 'session'
    fields = ['is_closed']

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside tbl session form template.
        """

        context = super(OpenSessionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def form_valid(self, form):
        self.object.is_closed = False
        messages.success(self.request, _('TBL session open successfully.'))
        return super(OpenSessionView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'TBLSessions:list',
            kwargs={'slug': discipline.slug}
        )

        return success_url



class ShowSessionView(LoginRequiredMixin,
                      PermissionMixin,
                      DetailView):
    """
    View to show a specific tbl session.
    """

    template_name = 'TBLSessions/details.html'
    context_object_name = 'session'
    permissions_required = [
        'show_sessions_permission',
        'show_tbl_session'
    ]

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_object(self):
        """
        Get the session discipline.
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline into tbl session context.
        """

        session = self.get_object()
        irat_datetime, grat_datetime = get_datetimes(session)

        context = super(ShowSessionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        return context
