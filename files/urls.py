from django.conf.urls import url
from . import views

app_name = 'files'
urlpatterns = [
    # /profile/<discipline.slug>/files/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/$',
        views.ListDisciplineFileView.as_view(),
        name='list'
    ),
    # /profile/<discipline.slug>/files/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/add/$',
        views.CreateDisciplineFileView.as_view(),
        name='create'
    ),
    # /profile/<discipline.slug>/groups/<file.id>/edit/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/(?P<pk>[0-9]+)/edit/$',
        views.EditDisciplineFileView.as_view(),
        name='update'
    ),
    # /profile/<discipline.slug>/files/<file.id>/delete/
    url(
        r'^profile/(?P<slug>[\w_-]+)/files/(?P<pk>[0-9]+)/delete/$',
        views.DeleteDisciplineFileView.as_view(),
        name='delete'
    ),
]
