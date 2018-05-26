from django.db.models import Q
from django.shortcuts import render
# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, ListView, UpdateView, FormView, DeleteView
)
from django.http import HttpResponseRedirect

# Application imoports
from TBLSessions.models import TBLSession
from disciplines.models import Discipline
from .forms import PeerReviewForm

# Get the custom user from settings
User = get_user_model()


class PeerReviewView(LoginRequiredMixin, ListView):
    """
    Class to read a profile user and his disciplines.
    """

    template_name = 'peer_review/peer.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super(PeerReviewView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['form'] = PeerReviewForm()

        return context

    def get_queryset(self):
        """
        List all students from discipline.
        """

        self.discipline = self.get_discipline()

        students = self.discipline.students.all()

        # Insert students into queryset
        queryset = []
        for student in students:
            queryset.append(student)

        return queryset

    def get_discipline(self):
        """
        Take the discipline that the group belongs to
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

    def get_peer_review(request):
        if request.POST:
            form = PeerReviewForm(request.POST)
            if form.is_valid():
                peer = form.save(commit=False)
                #peer.username_received = ??
                #peer.username_gave = User
                peer.save()
                #return redirect('post_detail', pk=post.pk)
            else:
                form = PostForm()
    #return render(request, '#', {'form': form})
