from django.conf.urls import url, include
from . import views_irat

app_name = 'exams'

iRAT_patterns = [
    # /iRAT/create/
    url(
        r'^iRAT/create/$',
        views_irat.CreateIRATView.as_view(),
        name='irat-create'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/exercises/...
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/exam/',
        include(iRAT_patterns)
    ),
]
