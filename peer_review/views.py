from django.shortcuts import render
# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, ListView, UpdateView, FormView, DeleteView
)

# Application imoports
from TBLSessions.models import TBLSession
from disciplines.models import Discipline

# Get the custom user from settings
User = get_user_model()


def peer(request):
    return render(request, 'peer_review/peer.html', {})


def home(request):
    return render(request, 'peer_review/teste.html', {})


class PeerReviewView(LoginRequiredMixin, ListView):
    """
    Class to read a profile user and his disciplines.
    """

    paginate_by = 6
    template_name = 'peer_review/peer.html'
    context_object_name = 'disciplines'

    def get_context_data(self, **kwargs):
        context = super(PeerReviewView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        return context

    def get_queryset(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        sessions = TBLSession.objects.filter(discipline=discipline)

        return sessions

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline
