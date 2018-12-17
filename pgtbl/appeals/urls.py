from django.urls import path, include
from . import views

app_name = 'appeals'

appeals_patterns = [
    path(
        '',
        views.AppealListView.as_view(),
        name='list'
    ),
    path(
        'create/',
        views.AppealCreateView.as_view(),
        name='create'
    ),
    path(
        '<int:pk>/detail/',
        views.AppealDetailView.as_view(),
        name='detail'
    ),
    path(
        '<int:pk>/submit-comment/',
        views.CommentCreateView.as_view(),
        name='submit-comment'
    ),
    path(
        '<int:pk>/update/',
        views.AppealUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:pk>/approve/',
        views.AppealApproveView.as_view(),
        name='approve'
    ),
    path(
        '<int:pk>/delete/',
        views.AppealDeleteView.as_view(),
        name='delete'
    ),
    path(
        '<int:appeal_id>/comment/<int:pk>/delete/',
        views.CommentDeleteView.as_view(),
        name='delete-comment'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:session_id>/appeals/',
        include(appeals_patterns)
    ),
]