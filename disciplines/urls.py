from django.conf.urls import url, include
from . import views

app_name = 'disciplines'

discipline_patterns = [
    # /profile/create-discipline/
    url(
        r'^create-discipline/$',
        views.CreateDisciplineView.as_view(),
        name='create'
    ),
    # /profile/list-discipline/
    url(
        r'^list-discipline/$',
        views.ListDisciplineView.as_view(),
        name='search'
    ),
    # /profile/update-discipline/<discipline.slug>/
    url(
        r'^update-discipline/(?P<slug>[\w_-]+)/$',
        views.UpdateDisciplineView.as_view(),
        name='update'
    ),
    # /profile/delete-discipline/<discipline.slug>/
    url(
        r'^delete-discipline/(?P<slug>[\w_-]+)/$',
        views.DeleteDisciplineView.as_view(),
        name='delete'
    ),
    # /profile/enter-discipline/<discipline.slug>/
    url(
        r'^enter-discipline/(?P<slug>[\w_-]+)/$',
        views.EnterDisciplineView.as_view(),
        name='enter'
    ),
    # /profile/<discipline.slug>/
    url(
        r'^(?P<slug>[\w_-]+)/$',
        views.ShowDisciplineView.as_view(),
        name='details'
    ),
    # /profile/<discipline.slug>/closed/
    url(
        r'^(?P<slug>[\w_-]+)/close/$',
        views.CloseDisciplineView.as_view(),
        name='close'
    ),
    # /profile/<discipline.slug>/students/
    url(
        r'^(?P<slug>[\w_-]+)/students/$',
        views.StudentListView.as_view(),
        name='students'
    ),
    # /profile/<discipline.slug>/students/1/remove
    url(
        r'^(?P<slug>[\w_-]+)/students/(?P<pk>[0-9]+)/remove/$',
        views.RemoveStudentView.as_view(),
        name='remove-student'
    ),
    # /profile/<discipline.slug>/students/add/
    url(
        r'^(?P<slug>[\w_-]+)/students/add/$',
        views.ListUsersView.as_view(),
        name='users'
    ),
    # /profile/<discipline.slug>/students/add/1/
    url(
        r'^(?P<slug>[\w_-]+)/students/add/(?P<pk>[0-9]+)/$',
        views.InsertStudentView.as_view(),
        name='insert-students'
    ),
    # /profile/<discipline.slug>/students/1/change
    url(
        r'^(?P<slug>[\w_-]+)/students/(?P<pk>[0-9]+)/change/$',
        views.ChangeStudentView.as_view(),
        name='change-student'
    ),
]

urlpatterns = [
    url(r'^profile/', include(discipline_patterns)),
]
