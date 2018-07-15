from django.urls import path, include
from . import views

app_name = 'modules'

session_patterns = [
    path(
        '',
        views.TBLSessionListView.as_view(),
        name='list'
    ),
    path(
        'create/',
        views.TBLSessionCreateView.as_view(),
        name='create'
    ),
    path(
        '<int:pk>/update/',
        views.TBLSessionUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:pk>/delete/',
        views.TBLSessionDeleteView.as_view(),
        name='delete'
    ),
    path(
        '<int:pk>/details/',
        views.TBLSessionDetailView.as_view(),
        name='details'
    ),
]

practical_patterns = [
    path(
        'practical-test/',
        views.PracticalTestDetailView.as_view(),
        name='practical-details'
    ),
    path(
        'practical-test/edit/',
        views.PracticalTestUpdateView.as_view(),
        name='practical-update'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/',
        include(session_patterns)
    ),
    path(
        'profile/<slug:slug>/sessions/<int:pk>/',
        include(practical_patterns)
    ),
]
