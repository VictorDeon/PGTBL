from django.conf.urls import url, include
from . import views

app_name = 'groups'

group_patterns = [
    # /profile/<discipline.slug>/groups/
    url(
        r'^$',
        views.ListGroupView.as_view(),
        name='list'
    ),
    # /profile/<discipline.slug>/groups/add/
    url(
        r'^add/$',
        views.CreateGroupView.as_view(),
        name='create'
    ),
    # /profile/<discipline.slug>/groups/1/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views.UpdateGroupView.as_view(),
        name='update'
    ),
    # /profile/<discipline.slug>/1/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.DeleteGroupView.as_view(),
        name='delete'
    ),
    # /profile/<discipline.slug>/groups/provide/
    url(
        r'^provide/$',
        views.ProvideGroupView.as_view(),
        name='provide'
    ),
    # /profile/<discipline.slug>/groups/<group.id>/students/
    url(
        r'^(?P<pk>[0-9]+)/students/$',
        views.ListAvailableStudentsView.as_view(),
        name='students'
    ),
    # /profile/<discipline.slug>/groups/<group.id>/students/<student.id>/add/
    url(
        r'^(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/add/$',
        views.InsertStudentView.as_view(),
        name='add-student'
    ),
    # /profile/<discipline.slug>/groups/<group.id>/students/<student.id>/remove/
    url(
        r'^(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/remove/$',
        views.RemoveStudentView.as_view(),
        name='remove-student'
    ),
]


urlpatterns = [
    url(r'^profile/(?P<slug>[\w_-]+)/groups/', include(group_patterns)),
]
