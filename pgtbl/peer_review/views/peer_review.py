from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession
from peer_review.forms import PeerReviewForm, PeerReviewAnswerForm


class PeerReviewView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    Peer Review test
    """

    template_name = "peer_review/peer_review.html"
    context_object_name = "students"

    permissions_required = ['show_peer_review_test']

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Get the discipline from url kwargs

        :return Discipline:
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the session from url kwargs

        :return TBLSession:
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_group(self):
        """
        Get the authenticated student group

        :return Group:
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if self.request.user in group.students.all():
                return group

    def get_context_data(self, **kwargs):
        """
        Insert discipline and session to pair review context data.

        :param kwargs:
        :return context to template:
        """

        context = super().get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['group'] = self.get_group()
        context['form'] = PeerReviewForm()
        context['answer_form'] = PeerReviewAnswerForm()

        return context

    def get_queryset(self):
        """
        Get the students to be assessed.

        :return Students to be assessed:
        """

        group = self.get_group()
        discipline = self.get_discipline()

        if group:
            students = group.students.exclude(
                pk=self.request.user.pk
            )
        elif self.request.user != discipline.teacher:
            messages.error(
                self.request,
                _("{0} has't group".format(self.request.user.get_short_name()))
            )

            return []
        else:
            return []

        return students