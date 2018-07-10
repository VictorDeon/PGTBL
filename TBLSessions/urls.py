from django.conf.urls import url, include
from . import views_session, views_practical

app_name = 'TBLSessions'

session_patterns = [
    # /
    url(
        r'^$',
        views_session.ListTBLSessionView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^add/$',
        views_session.CreateSessionView.as_view(),
        name='create'
    ),
    # <session.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views_session.EditSessionView.as_view(),
        name='update'
    ),
    # <session.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views_session.DeleteSessionView.as_view(),
        name='delete'
    ),
    # <session.id>/details/
    url(
        r'^(?P<pk>[0-9]+)/details/$',
        views_session.ShowSessionView.as_view(),
        name='details'
    ),
    # <session.id>/close/
    url(
        r'^(?P<pk>[0-9]+)/close/$',
        views_session.CloseSessionView.as_view(),
        name='close'
    ),
    # <session.id>/open/
    url(
        r'^(?P<pk>[0-9]+)/open/$',
        views_session.OpenSessionView.as_view(),
        name='open'
    ),

]

practical_patterns = [
    # practical-test/
    url(
        r'^practical-test/$',
        views_practical.PracticalTestDetailView.as_view(),
        name='practical-details'
    ),
    # practical-test/edit/
    url(
        r'^practical-test/edit/$',
        views_practical.PracticalTestUpdateView.as_view(),
        name='practical-update'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/sessions/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/',
        include(session_patterns)
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/',
        include(practical_patterns)
    ),
]
