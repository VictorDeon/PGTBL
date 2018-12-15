from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path(
        'notifications/',
        views.NotificationListView.as_view(),
        name="list"
    ),
    path(
        'notifications/delete-all',
        views.NotificationDeleteAllView.as_view(),
        name="delete-all"
    ),
    path(
        'notifications/<int:pk>/delete',
        views.NotificationDeleteView.as_view(),
        name="delete"
    )
]
