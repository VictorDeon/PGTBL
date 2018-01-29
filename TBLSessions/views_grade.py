from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from .models import TBLSession, Grade


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
