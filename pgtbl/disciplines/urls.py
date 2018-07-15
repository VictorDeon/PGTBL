from django.urls import path, include
from . import views

app_name = 'disciplines'

discipline_patterns = [
    path(
        'create-discipline/',
        views.DisciplineCreateView.as_view(),
        name='create'
    ),
    path(
        'list-discipline/',
        views.DisciplineListView.as_view(),
        name='search'
    ),
    path(
        'update-discipline/<slug:slug>/',
        views.DisciplineUpdateView.as_view(),
        name='update'
    ),
    path(
        'delete-discipline/<slug:slug>/',
        views.DisciplineDeleteView.as_view(),
        name='delete'
    ),
    path(
        'enter-discipline/<slug:slug>/',
        views.DisciplineEnterView.as_view(),
        name='enter'
    ),
    path(
        '<slug:slug>/details/',
        views.DisciplineDetailView.as_view(),
        name='details'
    ),
    path(
        '<slug:slug>/close/',
        views.DisciplineCloseView.as_view(),
        name='close'
    ),
]

student_patterns = [
    path(
        '',
        views.StudentListView.as_view(),
        name='students'
    ),
    path(
        '<int:pk>/remove/',
        views.StudentRemoveView.as_view(),
        name='remove-student'
    ),
    path(
        'add/',
        views.UsersListView.as_view(),
        name='users'
    ),
    path(
        'add/<int:pk>/',
        views.StudentInsertView.as_view(),
        name='insert-students'
    ),
    path(
        '<int:pk>/change/',
        views.StudentChangeView.as_view(),
        name='change-student'
    ),
]

urlpatterns = [
    path('profile/', include(discipline_patterns)),
    path('profile/<slug:slug>/students/', include(student_patterns))
]
