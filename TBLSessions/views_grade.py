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
from .forms import GradeForm


class GradeListView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to see all student grades of TBL sessions.
    """

    template_name = 'TBLSessions/grade_list.html'
    context_object_name = 'sessions'

    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_sessions(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        sessions = TBLSession.objects.filter(discipline=discipline)

        return sessions

    def get_session(self):
        """
        Get session by url query.
        """

        session_id = self.request.GET.get("session")

        if session_id == None or session_id == 'final-grade':
            return

        session = TBLSession.objects.get(
            discipline=self.get_discipline(),
            pk=session_id
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into session context data.
        """

        context = super(GradeListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['grades'] = self.get_queryset()
        context['final_grade'] = self.calcule_final_grade()
        context['sessions'] = self.get_sessions()
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

    def calcule_final_grade(self):
        """
        Calcule the student final grade.
        """

        final_grade = None

        return final_grade


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

    permissions_required = []

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
        Get student grade.
        """

        user = User.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        grade = Grade.objects.get(
            user=user
        )

        return grade

    def get_context_data(self, **kwargs):
        """
        Insert a discipline inside grade edit template.
        """

        context = super(GradeUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
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

        messages.error(
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

        success_url = reverse_lazy(
            'TBLSessions:grade-list',
            kwargs={'slug': discipline.slug}
        )

        return success_url
