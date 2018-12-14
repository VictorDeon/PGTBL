from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.models import Topic


class TopicListView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    View to see all forum topics
    """

    template_name = 'forum/list.html'
    paginate_by = 10
    context_object_name = 'topics'

    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the topic belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert some attributes into forum context data.
        """

        context = super(TopicListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context

    def get_queryset(self):
        """
        Get the appeals queryset from model database.
        """

        topics = Topic.objects.filter(
            discipline=self.get_discipline()
        )

        topics = self.search_topics(topics)

        return topics

    def search_topics(self, topics):
        """
        Search specific topic by title or author name
        """

        query = self.request.GET.get("q_info")

        if query:
            # Verify if topic title and author name contains the query specify
            # by user and filter all topics that satisfies this
            topics = topics.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query)
            ).distinct()

        return topics
