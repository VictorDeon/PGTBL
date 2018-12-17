from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.models import Topic, Answer


class AnswerDeleteView(LoginRequiredMixin,
                       PermissionMixin,
                       DeleteView):
    """
    View to delete a specific answer.
    """

    model = Answer

    permissions_required = ['edit_and_delete_topic_and_answer']

    def get_discipline(self):
        """
        Take the discipline that the topic belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_topic(self):
        """
        Get a specific topic to be deleted
        """

        topic = Topic.objects.get(
            pk=self.kwargs.get('topic_id', '')
        )

        return topic

    def get_object(self):
        """
        Get the specific answer from topic.
        """

        answer = Answer.objects.get(
            topic=self.get_topic(),
            pk=self.kwargs.get('pk', '')
        )

        return answer

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

        messages.success(self.request, _("Answer deleted successfully."))

        return success_url