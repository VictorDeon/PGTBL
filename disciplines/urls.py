from django.conf.urls import url
from . import views

app_name = 'disciplines'
urlpatterns = [
    # /profile/create_discipline/
    url(
        r'^profile/create-discipline/$',
        views.CreateDisciplineView.as_view(),
        name='create'
    ),
    # /profile/list-discipline/
    url(
        r'^profile/list-discipline/$',
        views.ListDisciplineView.as_view(),
        name='search'
    ),
    # /profile/update-discipline/discipline-name/
    url(
        r'^profile/update-discipline/(?P<slug>[\w_-]+)/$',
        views.UpdateDisciplineView.as_view(),
        name='update'
    ),
    # /profile/delete-discipline/discipline-name/
    url(
        r'^profile/delete-discipline/(?P<slug>[\w_-]+)/$',
        views.DeleteDisciplineView.as_view(),
        name='delete'
    ),
    # /profile/enter-discipline/discipline-name/
    url(
        r'^profile/enter-discipline/(?P<slug>[\w_-]+)/$',
        views.EnterDisciplineView.as_view(),
        name='enter'
    ),
    # /profile/discipline-name/
    url(
        r'^profile/(?P<slug>[\w_-]+)/$',
        views.ShowDisciplineView.as_view(),
        name='details'
    ),
    # /profile/discipline-name/closed/
    url(
        r'^profile/(?P<slug>[\w_-]+)/close/$',
        views.CloseDisciplineView.as_view(),
        name='close'
    ),
    # /profile/discipline-name/students/
    url(
        r'^profile/(?P<slug>[\w_-]+)/students/$',
        views.StudentListView.as_view(),
        name='students'
    ),
    # /profile/discipline-name/students/1/remove
    url(
        r'^profile/(?P<slug>[\w_-]+)/students/(?P<pk>[0-9]+)/remove/$',
        views.RemoveStudentView.as_view(),
        name='remove-student'
    ),
]
