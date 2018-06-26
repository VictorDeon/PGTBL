from django.conf.urls import url, include
from . import views

app_name = 'dashboard'

dashboard_patterns = [
    url(
        r'^dashboard/$',
        views.DashboardView.as_view(),
        name='list'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/',
        include(dashboard_patterns)
    ),
]
