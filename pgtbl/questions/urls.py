from django.conf.urls import url, include
from . import views

app_name = 'questions'

questions_patterns = [
    # /
    url(
        r'^$',
        views.ExerciseListView.as_view(),
        name='list'
    ),
    # /add-question/
    url(
        r'^add-question/$',
        views.CreateQuestionView.as_view(),
        name='create-question'
    ),
    # /question.id/edit/
    url(
        r'^(?P<question_id>[0-9]+)/edit/$',
        views.UpdateQuestionView.as_view(),
        name='update-question'
    ),
    # /question.id/delete/
    url(
        r'^(?P<question_id>[0-9]+)/delete/$',
        views.DeleteQuestionView.as_view(),
        name='delete-question'
    ),
]

exercise_patterns = [
    # /result/
    url(
        r'^result/$',
        views.ExerciseResultView.as_view(),
        name='exercise-result'
    ),
    # /result/csv/
    url(
        r'^result/csv/$',
        views.get_csv,
        name='exercise-result-csv'
    ),
    # /result/reset/
    url(
        r'^result/reset/$',
        views.ResetExerciseView.as_view(),
        name='exercise-reset'
    ),
    # /question/<question.id>/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views.AnswerQuestionView.as_view(),
        name='exercise-answer-question'
    )
]

irat_patterns = [
    # /
    url(
        r'^$',
        views.IRATView.as_view(),
        name='irat-list'
    ),
    # /edit-date/
    url(
        r'^edit-date/$',
        views.IRATDateUpdateView.as_view(),
        name='irat-date'
    ),
    # /edit-irat/
    url(
        r'^edit-irat/$',
        views.IRATUpdateView.as_view(),
        name='irat-update'
    ),
    # /result/
    url(
        r'^result/$',
        views.IRATResultView.as_view(),
        name='irat-result'
    ),
    # /question/<question.id>/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views.IRATAnswerQuestionView.as_view(),
        name='irat-answer-question'
    ),
]

grat_patterns = [
    # /
    url(
        r'^$',
        views.GRATView.as_view(),
        name='grat-list'
    ),
    # /edit-date/
    url(
        r'^edit-date/$',
        views.GRATDateUpdateView.as_view(),
        name='grat-date'
    ),
    # /edit-irat/
    url(
        r'^edit-irat/$',
        views.GRATUpdateView.as_view(),
        name='grat-update'
    ),
    # /result/
    url(
        r'^result/$',
        views.GRATResultView.as_view(),
        name='grat-result'
    ),
    # /question/<question.id>/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views.GRATAnswerQuestionView.as_view(),
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
