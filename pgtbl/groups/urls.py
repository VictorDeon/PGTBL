from django.conf.urls import url, include
from . import views

app_name = 'groups'

group_patterns = [
    # /
    url(
        r'^$',
        views.GroupListView.as_view(),
        name='list'
    ),
    # add/
    url(
        r'^add/$',
        views.GroupCreateView.as_view(),
        name='create'
    ),
    # <group.id>/edit/
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        views.GroupUpdateView.as_view(),
        name='update'
    ),
    # <group.id>/delete/
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.GroupDeleteView.as_view(),
        name='delete'
    ),
    # provide/
    url(
        r'^provide/$',
        views.GroupProvideView.as_view(),
        name='provide'
    ),
    # <group.id>/students/
    url(
        r'^(?P<pk>[0-9]+)/students/$',
        views.StudentListAvailableView.as_view(),
        name='students'
    ),
    # <group.id>/students/<student.id>/add/
    url(
        r'^(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/add/$',
        views.StudentInsertView.as_view(),
        name='add-student'
    ),
    # <group.id>/students/<student.id>/remove/
    url(
        r'^(?P<group_id>[0-9]+)/students/(?P<student_id>[0-9]+)/remove/$',
        views.StudentRemoveView.as_view(),
        name='remove-student'
    ),
]


urlpatterns = [
    # /profile/<discipline.slug>/groups/...
    url(r'^profile/(?P<slug>[\w_-]+)/groups/', include(group_patterns)),
]
