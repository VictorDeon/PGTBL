from django.urls import path, include
from . import views

app_name = 'questions'

questions_patterns = [
    path(
        'add-question/',
        views.CreateQuestionView.as_view(),
        name='create-question'
    ),
    path(
        '<int:question_id>/edit/',
        views.UpdateQuestionView.as_view(),
        name='update-question'
    ),
    path(
        '<int:question_id>/delete/',
        views.DeleteQuestionView.as_view(),
        name='delete-question'
    ),
]

irat_patterns = [
    path(
        '',
        views.IRATView.as_view(),
        name='irat-list'
    ),
    path(
        'edit-date/',
        views.IRATDateUpdateView.as_view(),
        name='irat-date'
    ),
    path(
        'edit-irat/',
        views.IRATUpdateView.as_view(),
        name='irat-update'
    ),
    path(
        'result/',
        views.IRATResultView.as_view(),
        name='irat-result'
    ),
    path(
        'question/<int:question_id>/answer-page/<int:question_page>/',
        views.IRATAnswerQuestionView.as_view(),
        name='irat-answer-question'
    ),
]

grat_patterns = [
    path(
        '',
        views.GRATView.as_view(),
        name='grat-list'
    ),
    path(
        'edit-date/',
        views.GRATDateUpdateView.as_view(),
        name='grat-date'
    ),
    path(
        'edit-irat/',
        views.GRATUpdateView.as_view(),
        name='grat-update'
    ),
    path(
        'result/',
        views.GRATResultView.as_view(),
        name='grat-result'
    ),
    path(
        'question/<int:question_id>/answer-page/<int:question_page>/',
        views.GRATAnswerQuestionView.as_view(),
        name='grat-answer-question'
    ),
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/questions/',
        include(questions_patterns)
    ),
    path(
        'profile/<slug:slug>/sessions/<int:pk>/irat/',
        include(irat_patterns)
    ),
    path(
        'profile/<slug:slug>/sessions/<int:pk>/grat/',
        include(grat_patterns)
    ),
]
