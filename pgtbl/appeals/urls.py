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
        '<int:pk>/update/',
        views.AppealUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:pk>/delete/',
        views.AppealDeleteView.as_view(),
        name='delete'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:session_id>/appeals/',
        include(appeals_patterns)
    ),
]