from django.conf.urls import url
from . import views_discipline
from . import views_sessions

app_name = 'files'
urlpatterns = [
    # /profile/<discipline.slug>/files/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/$',
        views_discipline.ListDisciplineFileView.as_view(),
        name='list'
    ),
    # /profile/<discipline.slug>/files/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/add/$',
        views_discipline.CreateDisciplineFileView.as_view(),
        name='create'
    ),
    # /profile/<discipline.slug>/files/<file.id>/edit/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/(?P<pk>[0-9]+)/edit/$',
        views_discipline.EditDisciplineFileView.as_view(),
        name='update'
    ),
    # /profile/<discipline.slug>/files/<file.id>/delete/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/(?P<pk>[0-9]+)/delete/$',
        views_discipline.DeleteDisciplineFileView.as_view(),
        name='delete'
    ),
    # /profile/<discipline.slug>/files/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/$',
        views_discipline.ListDisciplineFileView.as_view(),
        name='list'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/files/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/files/$',
        views_sessions.ListSessionFileView.as_view(),
        name='session-list'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/files/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/files/add/$',
        views_sessions.CreateSessionFileView.as_view(),
        name='session-create'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/files/<file.id>/edit/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/files/(?P<file_id>[0-9]+)/edit/$',
        views_sessions.EditSessionFileView.as_view(),
        name='session-update'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/files/<file.id>/delete/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/files/(?P<file_id>[0-9]+)/delete/$',
        views_sessions.DeleteSessionFileView.as_view(),
        name='session-delete'
    ),
]
