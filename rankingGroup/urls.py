from django.conf.urls import url, include
from . import views

app_name = 'ranking'

ranking_patterns = [
    # create-discipline/
    url(
        r'^ranking-group/$',
        views.ShowRankingGroupView.as_view(),
        name='create'
    ),

]

urlpatterns = [
    # /profile/...
    url(r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/', include(ranking_patterns)),
]
