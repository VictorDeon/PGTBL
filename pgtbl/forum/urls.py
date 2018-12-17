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
        '<slug:tag>/',
        views.TopicListView.as_view(),
        name='list-tagged'
    ),
    path(
        '<int:pk>/topic-detail/',
        views.TopicDetailView.as_view(),
        name='detail'
    ),
    path(
        '<int:pk>/submit-answer/',
        views.AnswerView.as_view(),
        name='submit-answer'
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
    path(
        '<int:topic_id>/answer/<int:pk>/delete/',
        views.AnswerDeleteView.as_view(),
        name='delete-answer'
    ),
    path(
        '<int:topic_id>/answer/<int:pk>/correct/',
        views.CorrectAnswerView.as_view(),
        name='correct-answer'
    )
]

urlpatterns = [
    path(
        'profile/<slug:slug>/forum/',
        include(forum_patterns)
    ),
]