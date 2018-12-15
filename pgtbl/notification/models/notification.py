from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

# Get the custom user from settings
from disciplines.models import Discipline

User = get_user_model()


class Notification(models.Model):
    """
    Create a notification model.
    """

    title = models.CharField(
        _('Title'),
        max_length=100,
        help_text=_("Discipline title")
    )

    description = models.TextField(
        _('Description'),
        help_text=_("Discipline description")
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Receiver'),
        related_name="notifications_received"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
        related_name="notifications_sent"
    )

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='notifications',
        null=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the notification is created."),
        auto_now_add=True
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return self.title

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
