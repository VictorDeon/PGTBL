from django.conf.urls import url
from . import views

app_name = 'disciplines'
urlpatterns = [
    # /profile/create_discipline/
    url(
        r'^profile/create_discipline/$',
        views.DisciplineCreationView.as_view(),
        name='create'
    ),
]
