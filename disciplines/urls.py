from django.conf.urls import url, include
from . import views

app_name = 'disciplines'

discipline_patterns = [
    # create-discipline/
    url(
        r'^create-discipline/$',
        views.CreateDisciplineView.as_view(),
        name='create'
    ),
    # list-discipline/
    url(
        r'^list-discipline/$',
        views.ListDisciplineView.as_view(),
        name='search'
    ),
    # update-discipline/<discipline.slug>/
    url(
        r'^update-discipline/(?P<slug>[\w_-]+)/$',
        views.UpdateDisciplineView.as_view(),
        name='update'
    ),
    # delete-discipline/<discipline.slug>/
    url(
        r'^delete-discipline/(?P<slug>[\w_-]+)/$',
        views.DeleteDisciplineView.as_view(),
        name='delete'
    ),
    # enter-discipline/<discipline.slug>/
    url(
        r'^enter-discipline/(?P<slug>[\w_-]+)/$',
        views.EnterDisciplineView.as_view(),
        name='enter'
    ),
    # <discipline.slug>/
    url(
        r'^(?P<slug>[\w_-]+)/$',
        views.ShowDisciplineView.as_view(),
        name='details'
    ),
    # <discipline.slug>/closed/
    url(
        r'^(?P<slug>[\w_-]+)/close/$',
        views.CloseDisciplineView.as_view(),
        name='close'
    ),
    # <discipline.slug>/attendance/
    url(
        r'^(?P<slug>[\w_-]+)/attendance/$',
        views.AttendanceRateView.as_view(),
        name='attendance'
    ),
    # <discipline.slug>/attendance/createNewAttendace
    url(
        r'^(?P<slug>[\w_-]+)/attendance/createNewAttendance/$',
        views.createAttendanceView.as_view(),
        name='createNewAttendance'
    ),
    url(
        r'^(?P<slug>[\w_-]+)/attendance/updateFormView/$',
        views.check_attended_students,
        name='updateFormView'
    ),
    # <discipline.slug>/attendance/download
    url(
        r'^(?P<slug>[\w_-]+)/attendance/download/$',
        views.get_attendancies_csv,
        name='download'
    ),
    # <discipline.slug>/students/
    url(
        r'^(?P<slug>[\w_-]+)/students/$',
        views.StudentListView.as_view(),
        name='students'
    ),
    # <discipline.slug>/students/<student.id>/remove
    url(
        r'^(?P<slug>[\w_-]+)/students/(?P<pk>[0-9]+)/remove/$',
        views.RemoveStudentView.as_view(),
        name='remove-student'
    ),
    # <discipline.slug>/students/add/
    url(
        r'^(?P<slug>[\w_-]+)/students/add/$',
        views.ListUsersView.as_view(),
        name='users'
    ),
    # <discipline.slug>/students/add/<student.id>/
    url(
        r'^(?P<slug>[\w_-]+)/students/add/(?P<pk>[0-9]+)/$',
        views.InsertStudentView.as_view(),
        name='insert-students'
    ),
    # <discipline.slug>/students/<student.id>/change
    url(
        r'^(?P<slug>[\w_-]+)/students/(?P<pk>[0-9]+)/change/$',
        views.ChangeStudentView.as_view(),
        name='change-student'
    ),
]

urlpatterns = [
    # /profile/...
    url(r'^profile/', include(discipline_patterns)),
]
