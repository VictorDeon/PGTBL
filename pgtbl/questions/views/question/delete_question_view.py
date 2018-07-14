from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.models import Question


class DeleteQuestionView(LoginRequiredMixin,
                         PermissionMixin,
                         DeleteView):
    """
    View to delete a specific question.
    """

    model = Question

    permissions_required = [
        'crud_question_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
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

    def get_object(self):
        """
        Take the specific question to delete.
        """

        question = Question.objects.get(
            session=self.get_session(),
            pk=self.kwargs.get('question_id', '')
        )

        return question

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()
        question = self.get_object()

        if question.is_exercise:
            success_url = reverse_lazy(
                'questions:list',
                kwargs={
                    'slug': discipline.slug,
                    'pk': session.id
                }
            )
        else:
            success_url = reverse_lazy(
                'questions:irat-list',
                kwargs={
                    'slug': discipline.slug,
                    'pk': session.id
                }
            )

        messages.success(self.request, _("Question deleted successfully."))

        return success_url
