from django.views.generic import DetailView
from core.models import News


class NewsDetailView(DetailView):
    """
    View to see the news detail
    """

    model = News
    template_name = 'news/details.html'
