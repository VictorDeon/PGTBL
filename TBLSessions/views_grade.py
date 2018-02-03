from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
    ListView, UpdateView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from accounts.models import User
from .models import TBLSession, Grade
from .utils import get_datetimes
from .forms import GradeForm


class GradeListView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to see all student grades of TBL sessions.
    """

    template_name = 'TBLSessions/grade_list.html'
    context_object_name = 'grades'

    permissions_required = ['show_tbl_session']

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the session by url kwargs.
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into session context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(GradeListView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def get_queryset(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        grades = Grade.objects.filter(
            session=self.get_session()
        )

        return grades


class GradeUpdateView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    Update student grade.
    """

    model = Grade
    template_name = 'TBLSessions/grade_form.html'
    context_object_name = 'grade'
    form_class = GradeForm

    permissions_required = ['only_teacher_can_change']

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the session by url kwargs.
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Get student grade.
        """

        user = User.objects.get(
            pk=self.kwargs.get('student_pk', '')
        )

        grade = Grade.objects.get(
            user=user
        )

        return grade

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside grade edit template.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(GradeUpdateView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def form_valid(self, form):
        """
        Return the form with valided fields.
        """

        if form.instance.irat > 10 or form.instance.irat < 0:
            return self.form_invalid(form)

        if form.instance.grat > 10 or form.instance.grat < 0:
            return self.form_invalid(form)

        if form.instance.practical > 10 or form.instance.practical < 0:
            return self.form_invalid(form)

        if form.instance.peer_review > 10 or form.instance.peer_review < 0:
            return self.form_invalid(form)

        messages.success(
            self.request,
            _("Grades updated successfully.")
        )

        return super(GradeUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Return the form with specific field errors.
        """

        messages.error(
            self.request,
            _("Grade need to be a number between 0 and 10.")
        )

        return super(GradeUpdateView, self).form_invalid(form)

    def get_success_url(self):
        """
        Get the success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'TBLSessions:grade-list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.pk
            }
        )

        return success_url
