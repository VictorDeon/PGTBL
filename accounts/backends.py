from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelBackend(BaseModelBackend):
    """
    Backend of User Model to enter email as a way to login to system
    beyond username.

    More information: djangoproject.../topics/auth/customizing
    """

    def authenticate(self, username=None, password=None):
        """
        Check the username or email and password and return a user.
        """

        if username is not None:
            try:
                # if username is a email, get it and return a user.
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass
