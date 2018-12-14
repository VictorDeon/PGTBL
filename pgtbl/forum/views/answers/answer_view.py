from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.forms import AnswerForm
from forum.models import Answer, Topic


class AnswerView(LoginRequiredMixin,
                 PermissionMixin,
                 CreateView):
    """
    View to create a answer to specific topic.
    """

    model = Answer
    template_name = 'forum/detail.html'
    form_class = AnswerForm
    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the forum belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_topic(self):
        """
        Get a specific topic to be answered
        """

        topic = Topic.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return topic

    def form_valid(self, form):
        """
        Receive the form already validated to create a topic.
        """

        form.instance.author = self.request.user
        form.instance.topic = self.get_topic()
        form.save()

        messages.success(self.request, _('Answer created successfully.'))

        return super(AnswerView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Redirect to form with form error.
        """

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
        topic = self.get_topic()

        success_url = reverse_lazy(
            'forum:detail',
            kwargs={
                'slug': discipline.slug,
                'pk': topic.pk
            }
        )

        return success_url