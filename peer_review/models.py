from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from tbl import settings

User = get_user_model()


class PeerReview(models.Model):

    session = models.PositiveSmallIntegerField(
        _('Session'),
        default=0,
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Student'),
        related_name=_('Student'),
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Reviewed_by'),
        related_name=_('Reviewed_by'),
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

        return '{0}: {1} - {2}'.format(self.student, self.feedback, self.score)

    class Meta:
        verbose_name = _('PeerReview')
        verbose_name_plural = _('PeerReviews')
        ordering = ['student', 'reviewed_by']
