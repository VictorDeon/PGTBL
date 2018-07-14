from django.conf.urls import url, include
from . import views

app_name = 'modules'

session_patterns = [
    # /
    url(
        r'^$',
        views.TBLSessionListView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^create/$',
        views.TBLSessionCreateView.as_view(),
        name='create'
    ),
    # <session.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/update/$',
        views.TBLSessionUpdateView.as_view(),
        name='update'
    ),
    # <session.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.TBLSessionDeleteView.as_view(),
        name='delete'
    ),
    # <session.id>/details/
    url(
        r'^(?P<pk>[0-9]+)/details/$',
        views.TBLSessionDetailView.as_view(),
        name='details'
    ),
]

practical_patterns = [
    # practical-test/
    url(
        r'^practical-test/$',
        views.PracticalTestDetailView.as_view(),
        name='practical-details'
    ),
    # practical-test/edit/
    url(
        r'^practical-test/edit/$',
        views.PracticalTestUpdateView.as_view(),
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
