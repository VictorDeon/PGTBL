from django.conf.urls import url, include
from . import views

app_name = 'ranking'

ranking_patterns = [
    url(
        r'^ranking-group/$',
        views.ShowRankingGroupView.as_view(),
        name='list'
    ),

]

urlpatterns = [
    # /profile/...
    url(r'^profile/(?P<slug>[\w_-]+)/', include(ranking_patterns)),
]
