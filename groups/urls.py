from django.conf.urls import url
from . import views

app_name = 'groups'
urlpatterns = [
    # /profile/nome-da-disciplina/groups/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/$',
        views.ListGroupView.as_view(),
        name='list'
    ),
    # /profile/nome-da-disciplina/groups/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/add/$',
        views.CreateGroupView.as_view(),
        name='create'
    ),
]
