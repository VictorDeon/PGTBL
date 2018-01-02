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
from TBLSessions.models import TBLSession
from .models import Alternative, Question
from .forms import QuestionForm


class ExerciseListView(LoginRequiredMixin,
                       ListView):
    """
    View to see all the questions that the students will answer.
    Exercise list to answer.
    """

    template_name = 'questions/list.html'
    paginate_by = 1
    context_object_name = 'questions'

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session and form into exercise list context data.
        """

        context = super(ExerciseListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['form'] = QuestionForm()
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        session = self.get_session()

        questions = Question.objects.filter(
            session=session,
        )

        return questions
