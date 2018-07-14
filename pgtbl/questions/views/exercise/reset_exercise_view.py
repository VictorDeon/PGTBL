from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.contrib import messages
from django.shortcuts import redirect

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.models import ExerciseSubmission


class ResetExerciseView(LoginRequiredMixin,
                        PermissionMixin,
                        RedirectView):
    """
    Reset the exercise.
    """

    permissions_required = [
        'show_questions_permission'
    ]

    def get_discipline(self):
        """
        Get discipline by url slug
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

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        submissions = ExerciseSubmission.objects.filter(
            session=self.get_session(),
            user=self.request.user
        )

        return submissions

    def get_success_url(self):
        """
        Get the success url to redirect to.
        """

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url

    def get(self, request, *args, **kwargs):
        """
        Reset exercise list.
        """

        submissions = self.get_queryset()

        for submission in submissions:
            submission.delete()

        messages.success(
            self.request,
            _("Exercise list reseted successfully.")
        )

        return redirect(self.get_success_url())
