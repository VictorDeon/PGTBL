from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
  # /
  url(
      r'^$',
      views.HomePageView.as_view(),
      name="home"
  ),
  # /news/
  url(
      r'^news/$',
      views.NewsListView.as_view(),
      name="news"
  ),
  # /news/important/
  url(
      r'^news/tag/(?P<tag>[\w_-]+)/$',
      views.NewsListView.as_view(),
      name="news-tag"
  ),
  # /news/new01/
  url(
      r'^news/(?P<slug>[\w_-]+)/$',
      views.NewsDetailView.as_view(),
      name="news-details"
  ),
]
