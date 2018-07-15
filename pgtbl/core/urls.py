from django.urls import path, include
from . import views

app_name = 'core'

news_patterns = [
    path(
        '',
        views.NewsListView.as_view(),
        name="news"
    ),
    path(
        'tag/<slug:tag>/',
        views.NewsListView.as_view(),
        name="news-tag"
    ),
    path(
        '<slug:slug>/details/',
        views.NewsDetailView.as_view(),
        name="news-details"
    ),
]

urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name="home"
    ),
    path('news/', include(news_patterns)),
]
