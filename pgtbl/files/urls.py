from django.urls import path, include
from . import views

app_name = 'files'

discipline_patterns = [
    path(
        '',
        views.DisciplineFileListView.as_view(),
        name='list'
    ),
    path(
        'create/',
        views.DisciplineFileCreateView.as_view(),
        name='create'
    ),
    path(
        '<int:pk>/update/',
        views.DisciplineFileUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:pk>/delete/',
        views.DisciplineFileDeleteView.as_view(),
        name='delete'
    ),
]

module_patterns = [
    path(
        '',
        views.ModuleFileListView.as_view(),
        name='module-list'
    ),
    path(
        'create/',
        views.ModuleFileCreateView.as_view(),
        name='module-create'
    ),
    path(
        '<int:file_id>/update/',
        views.ModuleFileUpdateView.as_view(),
        name='module-update'
    ),
    path(
        '<int:file_id>/delete/',
        views.ModuleFileDeleteView.as_view(),
        name='module-delete'
    ),
]


urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/files/',
        include(module_patterns)
    ),

    path(
        'profile/<slug:slug>/files/',
        include(discipline_patterns)
    ),
]
