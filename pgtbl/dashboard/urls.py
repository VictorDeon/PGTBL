from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path(
        'profile/<slug:slug>/sessions/<int:pk>/dashboard/',
        views.DashboardDetailView.as_view(),
        name='dashboard'
    )
]