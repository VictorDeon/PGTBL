from django.contrib.auth.views import login, logout
from django.urls import path, include
from . import views

app_name = 'accounts'

profile_patterns = [
    # /
    path(
        '',
        views.UserDetailView.as_view(),
        name='profile'
    ),
    # update/
    path(
        'update/',
        views.UserUpdateView.as_view(),
        name='update-user'
    ),
    # delete/
    path(
        'delete/',
        views.UserDeleteView.as_view(),
        name='delete-user'
    ),
    # password-update/
    path(
        'password-update/',
        views.PasswordUpdateView.as_view(),
        name='update-password'
    ),
]

urlpatterns = [
    # /login/
    path(
        'login/',
        login,
        # Subscribe the template_name of login view from django.
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    # /logout/
    path(
        'logout/',
        logout,
        # Subscribe the next_page of logout view from django.
        # The next_page redirect the view to the home page.
        {'next_page': 'core:home'},
        name='logout'
    ),
    # /register/
    path(
        'register/',
        views.UserCreateView.as_view(),
        name='register'
    ),
    # /reset-password/
    path(
        'reset-password/',
        views.ResetPasswordView.as_view(),
        name="reset-password"
    ),
    # /confirm-new-password/<key>/
    path(
        'confirm-new-password/<slug:key>/',
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm"
    ),
    # /profile/...
    path('profile/', include(profile_patterns)),
]
