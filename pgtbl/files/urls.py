from django.conf.urls import url, include
from . import views_discipline
from . import views_sessions

app_name = 'files'

discipline_patterns = [
    # /
    url(
        r'^$',
        views_discipline.ListDisciplineFileView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^add/$',
        views_discipline.CreateDisciplineFileView.as_view(),
        name='create'
    ),
    # <file.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views_discipline.EditDisciplineFileView.as_view(),
        name='update'
    ),
    # <file.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views_discipline.DeleteDisciplineFileView.as_view(),
        name='delete'
    ),
]

session_patterns = [
    # /
    url(
        r'^$',
        views_sessions.ListSessionFileView.as_view(),
        name='session-list'
    ),
    # add/
    url(
        r'^add/$',
        views_sessions.CreateSessionFileView.as_view(),
        name='session-create'
    ),
    # <file.id>/edit/
    url(
        r'^(?P<file_id>[0-9]+)/edit/$',
        views_sessions.EditSessionFileView.as_view(),
        name='session-update'
    ),
    # <file.id>/delete/
    url(
        r'^(?P<file_id>[0-9]+)/delete/$',
        views_sessions.DeleteSessionFileView.as_view(),
        name='session-delete'
    ),
]


urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/files/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/files/',
        include(session_patterns)
    ),

    # /profile/<discipline.slug>/files/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/',
        include(discipline_patterns)
    ),
]
