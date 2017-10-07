from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from .models import News


class HomePageView(ListView):
    """
    Home page of application.
    """

    template_name = 'core/home.html'
    # object queryset name that appears in the templates
    context_object_name = 'news_list'

    def get_queryset(self):
        """
        Get the specific queryset from model database.
        """

        # Get the last two news created
        queryset = News.objects.all()[:2]
        return queryset

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        # Get the initial context from IndexView (paginator, page_obj,
        # is_paginated, context_object_name especify or object_list)
        context = super(HomePageView, self).get_context_data()
        # Insert home and logged variables to template
        context['home'] = True
        context['logged'] = False
        return context


class ForgetPasswordView(TemplateView):
    """
    Page to send new password to email.
    """

    template_name = 'core/password.html'

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        context = super(ForgetPasswordView, self).get_context_data()
        context['home'] = False
        context['logged'] = False
        return context


class NewsListView(ListView):
    paginate_by = 6
    template_name = 'core/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        """
        Get the specific queryset from model database.
        """

        queryset = News.objects.all()
        # Get the tag by key argument from url
        tag = self.kwargs.get('tag', '')
        if tag:
            # Verify if the tag url slug contains the specific tag and get all
            # elemente with that tag
            queryset = queryset.filter(tags__slug__icontains=tag)
        # return searched news
        queryset = search_news(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        context = super(NewsListView, self).get_context_data()
        context['home'] = False
        context['logged'] = False
        # Get the tag by key argument from url
        tag = self.kwargs.get('tag', '')
        if tag:
            context['tag'] = tag
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'core/news_details.html'


def search_news(request, news_list):
    """
    Search from news list the specific news
    """

    query = request.GET.get("q_info")
    if query:
        # Verify if news title and content contains the query specify by user
        # and filter all news that satisfies this
        news_list = news_list.filter(
                        Q(title__icontains=query) |
                        Q(content__icontains=query)
                    ).distinct()
    return news_list
