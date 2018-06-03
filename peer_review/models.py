from django.utils.translation import ugettext_lazy as _
from django.db import models


class PeerReview(models.Model):

    session = models.PositiveSmallIntegerField(
        _('Session'),
        default=0,
    )

    student = models.CharField(
        _('Student'),
        max_length=30,
    )

    reviewed_by = models.CharField(
        _('Reviewed by'),
        max_length=30,
    )

    feedback = models.TextField(
        _('Feedback'),
        help_text=_('Feedback about your teammate ')
    )

    score = models.PositiveSmallIntegerField(
        _('Score'),
        blank=True,
        help_text=_("Score your teammate")
    )


    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}'.format(self.student)

    class Meta:
        verbose_name = _('PeerReview')
        verbose_name_plural = _('PeerReviews')
        ordering = ['student', 'reviewed_by']
