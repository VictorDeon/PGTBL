from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession


class PairReviewView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    Pair Review test
    """

    template_name = "pair_review/pair_review.html"
    paginate_by = 10
    context_object_name = "students"

    permissions_required = []

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

        return context

    def get_queryset(self):
        """
        Get the students to be assessed.

        :return Students to be assessed:
        """

        group = self.get_group()

        if group:
            students = group.students.exclude(
                pk=self.request.user.pk
            )
        else:
            messages.error(
                self.request,
                _("{0} has't group".format(self.request.user.get_short_name()))
            )

            return []

        return students