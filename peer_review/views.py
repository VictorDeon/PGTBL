from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, FormView
)

# Application imports
from TBLSessions.models import TBLSession
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from peer_review.models import PeerReview
from .forms import PeerReviewForm

# Get the custom user from settings
User = get_user_model()


class PeerReviewView(LoginRequiredMixin,
                     PermissionMixin,
                     FormView):
    """
    Working with form to create a peer review
    """

    template_name = 'peer_review/peer.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = PeerReviewForm
    permissions_required = [
        'only_student_can_change'
    ]

    def form_valid(self, form):

        """
        Receive the form already validated to create an Peer Review
        """

        session = self.get_session().id
        username_gave = form.cleaned_data.get('username_gave')
        username_received = form.cleaned_data.get('username_received')
        feedback = form.cleaned_data.get('feedback')
        score = form.cleaned_data.get('score')

        peer_review = self.return_existent_review(username_gave, username_received, session)

        peer_review.username_gave = username_gave
        peer_review.username_received = username_received
        peer_review.feedback = feedback
        if score is None:
            peer_review.score = 0
        else:
            peer_review.score = score
        peer_review.session = session
        peer_review.save()

        return super(PeerReviewView, self).form_valid(peer_review)

    def return_existent_review(self, username_gave, username_received, session):

        """
        Check if peer review already exists
        """

        try:
            query = PeerReview.objects.get(
                username_gave=username_gave,
                username_received=username_received,
                session=session,
            )
            peer_review = query
        except PeerReview.DoesNotExist:
            peer_review = PeerReview()

        return peer_review

    def get_context_data(self, **kwargs):
        context = super(PeerReviewView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['students'] = self.get_all_students(self.get_discipline())
        context['form'] = PeerReviewForm()

        return context

    def get_discipline(self):
        """
        Get the specific discipline.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the group belongs to
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_all_students(self, discipline):
        """
        Get students from dicipline
        """
        students = discipline.students.all()

        return students
