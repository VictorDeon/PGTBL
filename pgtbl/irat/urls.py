from django.urls import path, include
from . import views

app_name = 'irat'

irat_patterns = [
    path(
        '',
        views.IRATView.as_view(),
        name='list'
    ),
    path(
        'edit-date/',
        views.IRATDateUpdateView.as_view(),
        name='date'
    ),
    path(
        'edit-irat/',
        views.IRATUpdateView.as_view(),
        name='update'
    ),
    path(
        'result/',
        views.IRATResultView.as_view(),
        name='result'
    ),
    path(
        'question/<int:question_id>/answer-page/<int:question_page>/',
        views.IRATAnswerQuestionView.as_view(),
        name='answer-question'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/irat/',
        include(irat_patterns)
    )
]
