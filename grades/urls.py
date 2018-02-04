from django.conf.urls import url, include
from . import views

app_name = 'grades'

grade_patterns = [
    # /
    url(
        r'^$',
        views.GradeListView.as_view(),
        name='list'
    ),
    # /<student.id>/edit/
    url(
        r'^(?P<student_pk>[0-9]+)/edit/$',
        views.GradeUpdateView.as_view(),
        name='update'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/grades/
    url(
        r'^profile/(?P<slug>[\w_-]+)/grades/',
        views.GradeResultView.as_view(),
        name='result'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/grades/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/grades/',
        include(grade_patterns)
    ),
]
