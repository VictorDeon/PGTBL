from django.urls import path, include
from . import views

app_name = 'forum'

forum_patterns = [
    path(
        '',
        views.TopicListView.as_view(),
        name='list'
    ),
    path(
        'create-topic/',
        views.TopicCreateView.as_view(),
        name='create'
    ),
    path(
        '<int:pk>/topic-detail/',
        views.TopicDetailView.as_view(),
        name='detail'
    ),
    path(
        '<int:pk>/update-topic/',
        views.TopicUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:pk>/delete-topic/',
        views.TopicDeleteView.as_view(),
        name='delete'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/forum/',
        include(forum_patterns)
    ),
]