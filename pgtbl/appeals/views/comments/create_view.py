from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from appeals.forms import CommentForm
from appeals.models import Comment, Appeal
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession


class CommentCreateView(LoginRequiredMixin,
                        PermissionMixin,
                        CreateView):
    """
    View to create a comment to specific appeal.
    """

    model = Comment
    template_name = 'appeals/detail.html'
    form_class = CommentForm
    permissions_required = ['show_appeals']

    def get_discipline(self):
        """
        Take the discipline that the forum belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the appeal belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('session_id', '')
        )

        return session

    def get_appeal(self):
        """
        Get a specific appeal to be commented
        """

        appeal = Appeal.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return appeal

    def form_valid(self, form):
        """
        Receive the form already validated to create a topic.
        """

        form.instance.author = self.request.user
        form.instance.appeal = self.get_appeal()
        form.save()

        messages.success(self.request, _('Comment created successfully.'))

        return super(CommentCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to form with form error.
        """

        print(form)

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()
        appeal = self.get_appeal()

        success_url = reverse_lazy(
            'appeals:detail',
            kwargs={
                'slug': discipline.slug,
                'session_id': session.pk,
                'pk': appeal.pk
            }
        )

        return success_url