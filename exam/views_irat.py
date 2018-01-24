from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from .forms import iRATForm
from .models import iRAT

# Get the custom user from settings
User = get_user_model()


class CreateIRATView(LoginRequiredMixin,
                     PermissionMixin,
                     CreateView):
    """
    Create a iRAT test.
    """

    model = iRAT
    template_name = 'exams/irat_create.html'
    form_class = iRATForm

    permissions_required = []

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'TBLSessions:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline by kwargs url.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session by kwargs url.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def form_valid(self, form):
        """
        Receive the form already validated to create a group.
        """

        form.instance.session = self.get_session()
        form.save()


        return super(CreateIRATView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to group list with error.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return super(CreateIRATView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Insert a discipline and session inside iRAT form.
        """

        context = super(CreateIRATView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        messages.success(self.request, _('iRAT test created successfully.'))

        success_url = reverse_lazy(
            'TBLSessions:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url
