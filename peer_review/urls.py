from django.conf.urls import url

from . import views

app_name = 'peer_review'

urlpatterns = [
    url(
        r'^peer',
        views.peer,
        name='peer'
    ),
]