from django.urls import path, include
from . import views

app_name = 'practical'

practical_patterns = [
    path(
        '',
        views.PracticalTestDetailView.as_view(),
        name='details'
    ),
    path(
        'edit/',
        views.PracticalTestUpdateView.as_view(),
        name='update'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/practical-test/',
        include(practical_patterns)
    ),
]