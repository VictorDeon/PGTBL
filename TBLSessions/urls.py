from django.conf.urls import url
from . import views

app_name = 'TBLSessions'
urlpatterns = [
    # /profile/<discipline.slug>/sessions/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/$',
        views.ListTBLSessionView.as_view(),
        name='list'
    ),
    # /profile/<discipline.slug>/sessions/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/add/$',
        views.CreateSessionView.as_view(),
        name='create'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/edit/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/edit/$',
        views.EditSessionView.as_view(),
        name='update'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/delete/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/delete/$',
        views.DeleteSessionView.as_view(),
        name='delete'
    ),
    # /profile/<discipline.slug>/sessions/<session.id>/details/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/details/$',
        views.ShowSessionView.as_view(),
        name='details'
    ),
]
