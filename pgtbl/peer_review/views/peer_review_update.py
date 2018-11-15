from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from peer_review.forms import PeerReviewForm


class PeerReviewUpdateView(LoginRequiredMixin,
                           PermissionMixin,
                           UpdateView):
    """
    Update the Pair Review available and weight
    """

    model = TBLSession
    template_name = "peer_review/peer_review.html"
    form_class = PeerReviewForm

    permissions_required = ['crud_peer_review']

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
        Get the specific discipline

        :return Discipline:
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the specific session

        :return: TBLSession
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_success_url(self):
        """
        Get success url to redirect.

        :return String:
        """

        success_url = reverse_lazy(
            'peer_review:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url

    def form_valid(self, form):
        """
        Return the form with fields valided.

        :param form:
        :return HttpResponseRedirect:
        """

        messages.success(self.request, _("Pair Review updated successfully."))

        return super(PeerReviewUpdateView, self).form_valid(form)