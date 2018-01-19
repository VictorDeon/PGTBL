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
    # /result/
    url(
        r'^result/$',
        views.ExerciseResultView.as_view(),
        name='result'
    ),
    # /result/csv/
    url(
        r'^result/csv/$',
        views.get_csv,
        name='result-csv'
    ),
    # /add-question/
    url(
        r'^add-question/$',
        views.CreateQuestionView.as_view(),
        name='create-question'
    ),
    # /question/question.id/edit/
    url(
        r'^question/(?P<question_id>[0-9]+)/edit/$',
        views.UpdateQuestionView.as_view(),
        name='update-question'
    ),
    # /question/question.id/delete/
    url(
        r'^question/(?P<question_id>[0-9]+)/delete/$',
        views.DeleteQuestionView.as_view(),
        name='delete-question'
    ),
    # /question/question.id/answer-page/<page_obj.number>/
    url(
        r'^question/(?P<question_id>[0-9]+)/answer-page/(?P<question_page>[0-9]+)/$',
        views.AnswerQuestionView.as_view(),
        name='answer-question'
    )
]

alternatives_patterns = []

urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/exercises/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/exercises/',
        include(questions_patterns)
    ),
]
