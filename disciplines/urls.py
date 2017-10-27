from django.conf.urls import url
from . import views

app_name = 'disciplines'
urlpatterns = [
    # /profile/create_discipline/
    url(
        r'^profile/create-discipline/$',
        views.DisciplineCreationView.as_view(),
        name='create'
    ),
    # /profile/update-discipline/discipline-name
    url(
        r'^profile/update-discipline/(?P<slug>[\w_-]+)/$',
        views.DisciplineUpdateView.as_view(),
        name='update'
    ),
    # /profile/delete-discipline/discipline-name
    url(
        r'^profile/delete-discipline/(?P<slug>[\w_-]+)/$',
        views.DisciplineDeleteView.as_view(),
        name='delete'
    ),
]
