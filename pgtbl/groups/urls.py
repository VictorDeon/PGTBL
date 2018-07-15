from django.urls import path, include
from . import views

app_name = 'groups'

group_patterns = [
    path(
        '',
        views.GroupListView.as_view(),
        name='list'
    ),
    path(
        'add/',
        views.GroupCreateView.as_view(),
        name='create'
    ),
    path(
        '<int:pk>/edit/',
        views.GroupUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:pk>/delete/',
        views.GroupDeleteView.as_view(),
        name='delete'
    ),
    path(
        'provide/',
        views.GroupProvideView.as_view(),
        name='provide'
    ),
    path(
        '<int:pk>/students/',
        views.StudentListAvailableView.as_view(),
        name='students'
    ),
    path(
        '<int:group_id>/students/<int:student_id>/add/',
        views.StudentInsertView.as_view(),
        name='add-student'
    ),
    path(
        '<int:group_id>/students/<int:student_id>/remove/',
        views.StudentRemoveView.as_view(),
        name='remove-student'
    ),
]


urlpatterns = [
    path('profile/<slug:slug>/groups/', include(group_patterns))
]
