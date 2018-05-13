# Django app
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView,
    ListView, FormView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q

# Core app
from core.permissions import ModelPermissionMixin, PermissionMixin
from core.generics import ObjectRedirectView
from core.utils import order

# Ranking app
from .models import RankingGroup

class ShowRankingGroupView(LoginRequiredMixin,
                           PermissionMixin,
                           DetailView):

    """
    View to ranking_group .
    """
    template_name = 'rankingGroup/list.html'
    context_object_name = 'ranking'
    permissions_required = [
        'show_ranking_permission'
    ]


    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the session discipline.
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session
