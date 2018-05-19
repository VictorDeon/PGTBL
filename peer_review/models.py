from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db import models

# App imports
from groups.models import Group


class PeerReview(models.Model):

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='peer_review'
    )

    title = models.CharField(
        _('Title'),
        max_length=200,
        help_text=_('Session title.')
    )

    feedback = models.TextField(
        _('Feedback'),
        help_text = _('Feedback about your teammate ')
    )

    score = models.PositiveSmallIntegerField(
        _("Score"),
        default = 0,
        blank = True,
        help_text = _("Score your teammate")
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}'.format(self.title)
