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
    paginate_by = 5
    context_object_name = 'topics'

    permissions_required = ['show_forum']

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
        context['tags'] = Topic.tags.all()

        tag = self.kwargs.get('tag', '')
        if tag:
            context['tag'] = tag

        return context

    def get_queryset(self):
        """
        Get the appeals queryset from model database.
        """

        topics = Topic.objects.filter(
            discipline=self.get_discipline()
        )

        topics = self.search_topics(topics)
        topics = self.filter_topics(topics)

        tag = self.kwargs.get('tag', '')

        if tag:
            topics = topics.filter(tags__slug__icontains=tag)

        return topics

    def filter_topics(self, topics):
        """
        Filter topics
        """

        filtered = self.request.GET.get('filter')
        if filtered == 'viewed':
            topics = topics.order_by('-views')
        elif filtered == 'commented':
            topics = topics.order_by('-qtd_answers')

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
