from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.models import Topic


class TopicDeleteView(LoginRequiredMixin,
                      PermissionMixin,
                      DeleteView):
    """
    View to delete a specific topic.
    """

    model = Topic

    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the forum belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_object(self):
        """
        Get the specific topic from discipline.
        """

        topic = Topic.objects.get(
            discipline=self.get_discipline(),
            pk=self.kwargs.get('pk', '')
        )

        return topic

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'forum:list',
            kwargs={
                'slug': discipline.slug
            }
        )

        messages.success(self.request, _("Topic deleted successfully."))

        return success_url