from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'accounts'
urlpatterns = [
    # /login/
    url(
        r'^login/$',
        login,
        # Subscribe the template_name of login view from django.
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    # /logout/
    url(
        r'^logout/$',
        logout,
        # Subscribe the next_page of logout view from django.
        # The next_page redirect the view to the home page.
        {'next_page': 'core:home'},
        name='logout'
    ),
    # /register/
    url(
        r'^register/$',
        views.RegisterView.as_view(),
        name='register'
    ),
    # /profile/
    url(
        r'^profile/$',
        views.ProfileView.as_view(),
        name='profile'
    ),
    # /profile/edit/
    url(
        r'^profile/edit/$',
        views.EditProfileView.as_view(),
        name='update-user'
    ),
    # /profile/edit-password/
    url(
        r'^profile/edit-password/$',
        views.EditPasswordView.as_view(),
        name="update-password"
    ),
    # /reset-password/
    url(
        r'^reset-password/$',
        views.reset_password,
        name="reset-password"
    ),
    # /confirm-new-password/
    url(
        r'^confirm-new-password/(?P<key>\w+)/$',
        views.reset_password_confirm,
        name="reset-password-confirm"
    ),
]
