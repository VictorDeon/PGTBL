from django.conf.urls import url, include
from . import views

app_name = 'questions'

questions_patterns = [
    # /
    url(
        r'^$',
        views.ExerciseListView.as_view(),
        name='list'
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
