from django.urls import path, include
from . import views

app_name = 'grat'

grat_patterns = [
    path(
        '',
        views.GRATView.as_view(),
        name='list'
    ),
    path(
        'edit-date/',
        views.GRATDateUpdateView.as_view(),
        name='date'
    ),
    path(
        'edit-irat/',
        views.GRATUpdateView.as_view(),
        name='update'
    ),
    path(
        'result/',
        views.GRATResultView.as_view(),
        name='result'
    ),
    path(
        'question/<int:question_id>/answer-page/<int:question_page>/',
        views.GRATAnswerQuestionView.as_view(),
        name='answer-question'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/grat/',
        include(grat_patterns)
    )
]
