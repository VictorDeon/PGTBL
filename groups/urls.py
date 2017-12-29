from django.conf.urls import url, include
from . import views

app_name = 'groups'

group_patterns = [
    # /
    url(
        r'^$',
        views.ListGroupView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^add/$',
        views.CreateGroupView.as_view(),
        name='create'
    ),
    # <group.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views.UpdateGroupView.as_view(),
        name='update'
    ),
    # <group.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.DeleteGroupView.as_view(),
        name='delete'
    ),
    # provide/
    url(
        r'^provide/$',
        views.ProvideGroupView.as_view(),
        name='provide'
    ),
    # <group.id>/students/
    url(
        r'^(?P<pk>[0-9]+)/students/$',
        views.ListAvailableStudentsView.as_view(),
        name='students'
    ),
    # <group.id>/students/<student.id>/add/
    url(
        r'^(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/add/$',
        views.InsertStudentView.as_view(),
        name='add-student'
    ),
    # <group.id>/students/<student.id>/remove/
    url(
        r'^(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/remove/$',
        views.RemoveStudentView.as_view(),
        name='remove-student'
    ),
]


urlpatterns = [
    # /profile/<discipline.slug>/groups/...
    url(r'^profile/(?P<slug>[\w_-]+)/groups/', include(group_patterns)),
]
