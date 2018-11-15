from django.urls import path, include
from . import views

app_name = 'exercises'

exercise_patterns = [
    path(
        '',
        views.ExerciseListView.as_view(),
        name='list'
    ),
    path(
        'result/',
        views.ExerciseResultView.as_view(),
        name='result'
    ),
path(
        'edit-exercise/',
        views.ExerciseUpdateView.as_view(),
        name='update'
    ),
    path(
        'result/csv/',
        views.get_csv,
        name='result-csv'
    ),
    path(
        'result/reset/',
        views.ResetExerciseView.as_view(),
        name='reset'
    ),
    path(
        'question/<int:question_id>/answer-page/<int:question_page>/',
        views.AnswerQuestionView.as_view(),
        name='answer-question'
    )
]

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/exercises/',
        include(exercise_patterns)
    )
]
