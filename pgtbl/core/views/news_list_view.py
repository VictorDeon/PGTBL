from django.views.generic import ListView
from django.db.models import Q
from core.models import News


class NewsListView(ListView):
    paginate_by = 6
    template_name = 'news/list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        """
        Get the all news from model database.
        """

        queryset = News.objects.all()

        # Get the tag by key argument from url
        tag = self.kwargs.get('tag', '')

        if tag:
            # Verify if the tag url slug contains the specific tag and get all
            # elemente with that tag
            queryset = queryset.filter(tags__slug__icontains=tag)

        # Get searched news
        queryset = self.search_news(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        context = super(NewsListView, self).get_context_data()
        context['home'] = False

        # Get the tag by key argument from url
        tag = self.kwargs.get('tag', '')
        if tag:
            context['tag'] = tag

        return context

    def search_news(self, news_list):
        """
        Search from news list the specific news
        """

        query = self.request.GET.get("q_info")

        if query:
            # Verify if news title and content contains the query specify
            # by user and filter all news that satisfies this
            news_list = news_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        return news_list
