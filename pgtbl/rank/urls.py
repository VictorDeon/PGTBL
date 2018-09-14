from django.urls import path
from . import views

app_name = 'rank'

urlpatterns = [
    path(
        'profile/<slug:slug>/rank/',
        views.GroupRankView.as_view(),
        name='group'
    ),
    path(
        'profile/<slug:slug>/hall-of-fame/',
        views.HallOfFameView.as_view(),
        name='hall-of-fame'
    )
]