from django.conf.urls import url, include
from . import views

app_name = 'core'

news_patterns = [
  # /
  url(
      r'^$',
      views.NewsListView.as_view(),
      name="news"
  ),
  # <tag>/
  url(
      r'^tag/(?P<tag>[\w_-]+)/$',
      views.NewsListView.as_view(),
      name="news-tag"
  ),
  # <new.slug>/
  url(
      r'^(?P<slug>[\w_-]+)/$',
      views.NewsDetailView.as_view(),
      name="news-details"
  ),
]

urlpatterns = [
    # /
    url(
        r'^$',
        views.HomePageView.as_view(),
        name="home"
    ),
    # /news/...
    url(r'^news/', include(news_patterns)),
]
