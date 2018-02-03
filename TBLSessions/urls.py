from django.conf.urls import url, include
from . import views, views_grade

app_name = 'TBLSessions'

session_patterns = [
    # /
    url(
        r'^$',
        views.ListTBLSessionView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^add/$',
        views.CreateSessionView.as_view(),
        name='create'
    ),
    # <session.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views.EditSessionView.as_view(),
        name='update'
    ),
    # <session.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.DeleteSessionView.as_view(),
        name='delete'
    ),
    # <session.id>/details/
    url(
        r'^(?P<pk>[0-9]+)/details/$',
        views.ShowSessionView.as_view(),
        name='details'
    ),
]

grade_patterns = [
    # /
    url(
        r'^$',
        views_grade.GradeListView.as_view(),
        name='grade-list'
    ),
    # /<student.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views_grade.GradeUpdateView.as_view(),
        name='grade-update'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/sessions/...
    url(r'^profile/(?P<slug>[\w_-]+)/sessions/', include(session_patterns)),
    # /profile/<discipline.slug>/grades/...
    url(r'^profile/(?P<slug>[\w_-]+)/grades/', include(grade_patterns)),
]
