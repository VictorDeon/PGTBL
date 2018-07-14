from django.conf.urls import url, include
from . import views

app_name = 'disciplines'

discipline_patterns = [
    # create-discipline/
    url(
        r'^create-discipline/$',
        views.DisciplineCreateView.as_view(),
        name='create'
    ),
    # list-discipline/
    url(
        r'^list-discipline/$',
        views.DisciplineListView.as_view(),
        name='search'
    ),
    # update-discipline/<discipline.slug>/
    url(
        r'^update-discipline/(?P<slug>[\w_-]+)/$',
        views.DisciplineUpdateView.as_view(),
        name='update'
    ),
    # delete-discipline/<discipline.slug>/
    url(
        r'^delete-discipline/(?P<slug>[\w_-]+)/$',
        views.DisciplineDeleteView.as_view(),
        name='delete'
    ),
    # enter-discipline/<discipline.slug>/
    url(
        r'^enter-discipline/(?P<slug>[\w_-]+)/$',
        views.DisciplineEnterView.as_view(),
        name='enter'
    ),
    # <discipline.slug>/
    url(
        r'^(?P<slug>[\w_-]+)/$',
        views.DisciplineDetailView.as_view(),
        name='details'
    ),
    # <discipline.slug>/closed/
    url(
        r'^(?P<slug>[\w_-]+)/close/$',
        views.DisciplineCloseView.as_view(),
        name='close'
    ),
]

student_patterns = [
    # /
    url(
        r'^$',
        views.StudentListView.as_view(),
        name='students'
    ),
    # <student.id>/remove
    url(
        r'^(?P<pk>[0-9]+)/remove/$',
        views.StudentRemoveView.as_view(),
        name='remove-student'
    ),
    # add/
    url(
        r'^add/$',
        views.UsersListView.as_view(),
        name='users'
    ),
    # add/<student.id>/
    url(
        r'^add/(?P<pk>[0-9]+)/$',
        views.StudentInsertView.as_view(),
        name='insert-students'
    ),
    # <student.id>/change
    url(
        r'^(?P<pk>[0-9]+)/change/$',
        views.StudentChangeView.as_view(),
        name='change-student'
    ),
]

urlpatterns = [
    # /profile/...
    url(r'^profile/', include(discipline_patterns)),
    # /profile/<discipline.slug>/students/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/students/',
        include(student_patterns)
    ),
]
