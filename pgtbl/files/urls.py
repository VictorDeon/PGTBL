from django.conf.urls import url, include
from . import views

app_name = 'files'

discipline_patterns = [
    # /
    url(
        r'^$',
        views.DisciplineFileListView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^create/$',
        views.DisciplineFileCreateView.as_view(),
        name='create'
    ),
    # <file.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/update/$',
        views.DisciplineFileUpdateView.as_view(),
        name='update'
    ),
    # <file.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.DisciplineFileDeleteView.as_view(),
        name='delete'
    ),
]

module_patterns = [
    # /
    url(
        r'^$',
        views.ModuleFileListView.as_view(),
        name='module-list'
    ),
    # create/
    url(
        r'^create/$',
        views.ModuleFileCreateView.as_view(),
        name='module-create'
    ),
    # <file.id>/update/
    url(
        r'^(?P<file_id>[0-9]+)/update/$',
        views.ModuleFileUpdateView.as_view(),
        name='module-update'
    ),
    # <file.id>/delete/
    url(
        r'^(?P<file_id>[0-9]+)/delete/$',
        views.ModuleFileDeleteView.as_view(),
        name='module-delete'
    ),
]


urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/files/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/files/',
        include(module_patterns)
    ),

    # /profile/<discipline.slug>/files/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/',
        include(discipline_patterns)
    ),
]
