from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models


class PasswordReset(models.Model):
    """
    Create a password reset key to reset and get a new password.
    """

    # User who requested the new password.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name="password_resets"
    )

    # Unique key to reset password.
    key = models.CharField(
        _('Key'),
        max_length=100,
        unique=True
    )

    # Date to create a link to reset password.
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    # Indicates if the link was already used to not be used again
    confirmed = models.BooleanField(
        _('Confirmed?'),
        default=False,
        blank=True
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0} - {1}'.format(self.user, self.created_at)

    class Meta:
        """
        Some information about user class.
        """

        verbose_name = _('New password')
        verbose_name_plural = _('New passwords')
        ordering = ['-created_at']
