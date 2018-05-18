from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db import models

# App imports
from groups.models import Group

class PeerReview(models.Model):

    group = models.ForeignKey(
    Group,
    on_delete = models.CASCADE,
    related_name = 'peer_review'
    )

    feedback = models.TextField()

    title = models.CharField(
        _('Title'),
        max_length=200,
        help_text=_('Session title.')
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}'.format(self.title)
