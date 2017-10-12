from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
  # Url to home page
  url(
      r'^$',
      views.HomePageView.as_view(),
      name="home"
  ),
  # Url to see the list of news
  url(
      r'^news/$',
      views.NewsListView.as_view(),
      name="news"
  ),
  # Url to see the list of news by specific tag
  url(
      r'^news/tag/(?P<tag>[\w_-]+)/$',
      views.NewsListView.as_view(),
      name="news-tag"
  ),
  # Url to see the specific news details
  url(
      r'^news/(?P<slug>[\w_-]+)/$',
      views.NewsDetailView.as_view(),
      name="news-details"
  ),
]
