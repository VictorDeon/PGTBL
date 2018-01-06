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

# Python imports
from random import sample


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
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        session = self.get_session()

        questions = Question.objects.filter(
            session=session,
            is_exercise=True
        )

        return questions


class CreateQuestionView(LoginRequiredMixin,
                         CreateView):
    """
    View to create a new question.
    """

    model = Question
    template_name = 'questions/add.html'
    form_class = QuestionForm

    def get_discipline(self):
        """
        Take the discipline that the question belongs to.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the TBL session that the question belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and session into add question template.
        """

        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def form_valid(self, form):
        """
        Receive the form already validated to create a new question.
        """

        form.instance.session = self.get_session()
        form.save()

        messages.success(self.request, _('Question created successfully.'))

        return super(CreateQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to form with form errors.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return super(CreateQuestionView, self).form_invalid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url
