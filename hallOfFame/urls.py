from django.conf.urls import url, include
from . import views

app_name = 'hallOfFame'

hall_patterns = [
    url(
        r'^hall-of-fame/$',
        views.ShowHallView.as_view(),
        name='list'
    ),

]

urlpatterns = [
        # /profile/...
        url(r'^profile/(?P<slug>[\w_-]+)/', include(hall_patterns)),
]
