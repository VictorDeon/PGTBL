"""
File to authentication settings.
"""

# Custom user profile
# Tell Django to use our custom user model
# instead of its built in default user model.
AUTH_USER_MODEL = 'accounts.User'

# Login and logout url
LOGIN_URL = 'accounts:login'
LOGOUT_URL = 'accounts:logout'

# Url to redirect after login
LOGIN_REDIRECT_URL = 'core:home'

# Backends from django
# This is used for any authentications (facebook, twitter, ...)
AUTHENTICATION_BACKENDS = (
    # Standard backend only with username
    'django.contrib.auth.backends.ModelBackend',
    # New backend with email and username
    'accounts.backends.ModelBackend'
)
