from django.contrib.auth.views import login, logout
from django.conf.urls import url, include
from . import views

app_name = 'accounts'

profile_patterns = [
    # /profile/
    url(
        r'^$',
        views.ProfileView.as_view(),
        name='profile'
    ),
    # /profile/edit/
    url(
        r'^edit/$',
        views.EditProfileView.as_view(),
        name='update-user'
    ),
    # /profile/edit-password/
    url(
        r'^edit-password/$',
        views.EditPasswordView.as_view(),
        name='update-password'
    ),
    # /profile/delete/
    url(
        r'^delete/$',
        views.DeleteProfileView.as_view(),
        name='delete-user'
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
        views.RegisterView.as_view(),
        name='register'
    ),
    # /reset-password/
    url(
        r'^reset-password/$',
        views.ResetPasswordView.as_view(),
        name="reset-password"
    ),
    # /confirm-new-password/3d9j230r2m98mr2398h9r2h39rhc9/
    url(
        r'^confirm-new-password/(?P<key>\w+)/$',
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm"
    ),
    # /profile/
    url(r'^profile/', include(profile_patterns)),
]
