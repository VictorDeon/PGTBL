from django.conf.urls import url, include
from . import views

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

urlpatterns = [
    # /profile/<discipline.slug>/sessions/...
    url(r'^profile/(?P<slug>[\w_-]+)/sessions/', include(session_patterns)),
]
