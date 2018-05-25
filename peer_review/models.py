from django.utils.translation import ugettext_lazy as _
from django.db import models


class PeerReview(models.Model):

    username_received = models.CharField(
        _('User'),
        max_length=30,
    )

    username_gave = models.CharField(
        _('User'),
        max_length=30,
    )

    feedback = models.TextField(
        _('Feedback'),
        help_text=_('Feedback about your teammate ')
    )

    score = models.PositiveSmallIntegerField(
        _("Score"),
        default=0,
        blank=True,
        help_text=_("Score your teammate")
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}'.format(self.username_received)

    class Meta:
        verbose_name = _('PeerReview')
        verbose_name_plural = _('PeerReviews')
        ordering = ['username_received', 'username_gave']
