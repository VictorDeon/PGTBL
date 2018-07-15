from django.urls import path, include
from . import views

app_name = 'grades'

grade_patterns = [
    path(
        '',
        views.GradeListView.as_view(),
        name='list'
    ),
    path(
        '<int:student_pk>/edit/',
        views.GradeUpdateView.as_view(),
        name='update'
    ),
    path(
        'session-csv/',
        views.get_module_grade_csv,
        name='session-csv'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/grades/final-csv/',
        views.get_final_grade_csv,
        name='final-csv'
    ),
    path(
        'profile/<slug:slug>/grades/',
        views.GradeResultView.as_view(),
        name='result'
    ),
    path(
        'profile/<slug:slug>/sessions/<int:pk>/grades/',
        include(grade_patterns)
    ),
]
