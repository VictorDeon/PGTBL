from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.forms import AnswerForm
from forum.models import Topic


class TopicDetailView(LoginRequiredMixin,
                      PermissionMixin,
                      DetailView):
    """
    View to show a specific topic.
    """

    model = Topic
    template_name = 'forum/detail.html'
    context_object_name = 'topic'
    permissions_required = ['show_forum']

    def get_discipline(self):
        """
        Take the discipline that the topic belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_object(self):
        """
        Get the specific topic.
        """

        topic = Topic.objects.get(
            discipline=self.get_discipline(),
            pk=self.kwargs.get('pk', '')
        )

        return topic

    def get_context_data(self, **kwargs):
        """
        Insert discipline into tbl session context.
        """

        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = AnswerForm()

        self.increment_views()

        return context

    def increment_views(self):
        """
        Increment views
        """

        topic = self.get_object()

        if topic.author != self.request.user:
            topic.views += 1
            topic.save()