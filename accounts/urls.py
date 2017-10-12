from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'accounts'
urlpatterns = [
    url(
        r'^logar/$',
        login,
        # Subscribe the template_name of login view from django.
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        logout,
        # Subscribe the next_page of logout view from django.
        # The next_page redirect the view to the home page.
        {'next_page': 'core:home'},
        name='logout'
    ),
    url(
        r'^register/$',
        views.RegisterView.as_view(),
        name='register'
    ),
]
