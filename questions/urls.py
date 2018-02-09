from django.conf.urls import url, include
from . import views_question, views_exercise, views_irat, views_grat

app_name = 'questions'

questions_patterns = [
    # /
    url(
        r'^$',
        views_question.ExerciseListView.as_view(),
        name='list'
    ),
    # /add-question/
    url(
        r'^add-question/$',
        views_question.CreateQuestionView.as_view(),
        name='create-question'
    ),
    # /question.id/edit/
    url(
        r'^(?P<question_id>[0-9]+)/edit/$',
        views_question.UpdateQuestionView.as_view(),
        name='update-question'
    ),
    # /question.id/delete/
    url(
        r'^(?P<question_id>[0-9]+)/delete/$',
        views_question.DeleteQuestionView.as_view(),
        name='delete-question'
    ),
]

exercise_patterns = [
    # /result/
    url(
        r'^result/$',
        views_exercise.ExerciseResultView.as_view(),
        name='exercise-result'
    ),
    # /result/csv/
    url(
        r'^result/csv/$',
        views_exercise.get_csv,
        name='exercise-result-csv'
    ),
    # /result/reset/
    url(
        r'^result/reset/$',
        views_exercise.ResetExerciseView.as_view(),
        name='exercise-reset'
    ),
    # /question/<question.id>/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views_exercise.AnswerQuestionView.as_view(),
        name='exercise-answer-question'
    )
]

irat_patterns = [
    # /
    url(
        r'^$',
        views_irat.IRATView.as_view(),
        name='irat-list'
    ),
    # /edit-date/
    url(
        r'^edit-date/$',
        views_irat.IRATDateUpdateView.as_view(),
        name='irat-date'
    ),
    # /edit-irat/
    url(
        r'^edit-irat/$',
        views_irat.IRATUpdateView.as_view(),
        name='irat-update'
    ),
    # /result/
    url(
        r'^result/$',
        views_irat.IRATResultView.as_view(),
        name='irat-result'
    ),
    # /result/csv/
    url(
        r'^result/csv/$',
        views_irat.get_csv,
        name='irat-result-csv'
    ),
    # /question/<question.id>/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views_irat.AnswerIRATQuestionView.as_view(),
        name='irat-answer-question'
    ),
]

grat_patterns = [
    # /
    url(
        r'^$',
        views_grat.GRATView.as_view(),
        name='grat-list'
    ),
    # /edit-date/
    url(
        r'^edit-date/$',
        views_grat.GRATDateUpdateView.as_view(),
        name='grat-date'
    ),
    # /edit-irat/
    url(
        r'^edit-irat/$',
        views_grat.GRATUpdateView.as_view(),
        name='grat-update'
    ),
    # # /result/
    # url(
    #     r'^result/$',
    #     views_grat.GRATResultView.as_view(),
    #     name='grat-result'
    # ),
    # # /result/csv/
    # url(
    #     r'^result/csv/$',
    #     views_grat.get_csv,
    #     name='grat-result-csv'
    # ),
    # /question/<question.id>/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views_grat.AnswerGRATQuestionView.as_view(),
        name='grat-answer-question'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/exercises/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/questions/',
        include(questions_patterns)
    ),
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/exercises/',
        include(exercise_patterns)
    ),
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/irat/',
        include(irat_patterns)
    ),
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/grat/',
        include(grat_patterns)
    ),
]
