from django.contrib.auth.views import login, logout
from django.conf.urls import url, include
from . import views

app_name = 'accounts'

profile_patterns = [
    # /
    url(
        r'^$',
        views.UserDetailView.as_view(),
        name='profile'
    ),
    # update/
    url(
        r'^update/$',
        views.UserUpdateView.as_view(),
        name='update-user'
    ),
    # delete/
    url(
        r'^delete/$',
        views.UserDeleteView.as_view(),
        name='delete-user'
    ),
    # password-update/
    url(
        r'^password-update/$',
        views.PasswordUpdateView.as_view(),
        name='update-password'
    ),
]

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
        views.UserCreateView.as_view(),
        name='register'
    ),
    # /reset-password/
    url(
        r'^reset-password/$',
        views.ResetPasswordView.as_view(),
        name="reset-password"
    ),
    # /confirm-new-password/<key>/
    url(
        r'^confirm-new-password/(?P<key>\w+)/$',
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm"
    ),
    # /profile/...
    url(r'^profile/', include(profile_patterns)),
]
