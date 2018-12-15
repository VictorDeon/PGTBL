from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from appeals.models import Appeal
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession


class AppealApproveView(LoginRequiredMixin,
                        PermissionMixin,
                        DeleteView):
    """
    View to define if appeals is approved or not.
    """

    model = Appeal

    permissions_required = ['approve_appeal']

    def get_discipline(self):
        """
        Take the discipline that the topic belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the appeals belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('session_id', '')
        )

        return session

    def get_object(self):
        """
        Get the specific appeal from tbl session of discipline.
        """

        session = self.get_session()

        appeal = Appeal.objects.get(
            session=session,
            pk=self.kwargs.get('pk', '')
        )

        return appeal

    def delete(self, request, *args, **kwargs):
        """
        Redirect to modify to correct answer
        """

        return self.approve_appeal()

    def approve_appeal(self):
        """
        Modify the appeal to approved
        """

        appeal = self.get_object()

        if not appeal.is_accept:
            appeal.is_accept = True
        else:
            appeal.is_accept = False

        appeal.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()
        appeal = self.get_object()

        success_url = reverse_lazy(
            'appeals:detail',
            kwargs={
                'slug': discipline.slug,
                'session_id': session.pk,
                'pk': appeal.pk
            }
        )

        if appeal.is_accept:
            messages.success(self.request, _("Appeal modify to approved with successfully."))
        else:
            messages.error(self.request, _("Appeal modify to disapproved with successfully."))

        return success_url