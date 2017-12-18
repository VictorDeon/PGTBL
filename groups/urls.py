from django.conf.urls import url
from . import views

app_name = 'groups'
urlpatterns = [
    # /profile/discipline-name/groups/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/$',
        views.ListGroupView.as_view(),
        name='list'
    ),
    # /profile/discipline-name/groups/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/add/$',
        views.CreateGroupView.as_view(),
        name='create'
    ),
    # /profile/discipline-name/groups/1/edit/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/(?P<pk>[0-9]+)/edit/$',
        views.UpdateGroupView.as_view(),
        name='update'
    ),
    # /profile/discipline-name/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/(?P<pk>[0-9]+)/delete/$',
        views.DeleteGroupView.as_view(),
        name='delete'
    ),
    # /profile/discipline-name/groups/provide/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/provide/$',
        views.ProvideGroupView.as_view(),
        name='provide'
    ),
    # /profile/discipline-name/groups/group-pk/students/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/(?P<pk>[0-9]+)/students/$',
        views.ListAvailableStudentsView.as_view(),
        name='students'
    ),
    # /profile/discipline-name/groups/group-pk/students/student-pk/add/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/add/$',
        views.InsertStudentView.as_view(),
        name='add-student'
    ),
    # /profile/discipline-name/groups/group-pk/students/student-pk/remove/
    url(
        r'^profile/(?P<slug>[\w_-]+)/groups/(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/remove/$',
        views.RemoveStudentView.as_view(),
        name='remove-student'
    ),
]
