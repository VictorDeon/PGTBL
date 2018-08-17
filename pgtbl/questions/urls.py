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

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/questions/',
        include(questions_patterns)
    )
]
