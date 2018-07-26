from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from groups.models import Group
from modules.models import TBLSession


class PairReviewSubmission(models.Model):
    """
    Create a pair review test.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name=_("TBL Session"),
        related_name="pair_review_submissions"
    )

    score = models.PositiveIntegerField(
        _("Score"),
        default=0,
        help_text=_("Pair Review score to specific student")
    )

    comment = models.TextField(
        _("Comment"),
        help_text=_("Comment about the assessed student.")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Student who is evaluating"),
        related_name="pair_review_created_submissions"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Student being assessed"),
        related_name="pair_review_received_submissions"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_('Group'),
        related_name="pair_review_submissions"
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the submission is created."),
        auto_now_add=True
    )

    def __str__(self):
        """
        Alternative of question string.
        """

        obj = "{0}: {1} - {2}".format(
            self.user.get_short_name(),
            self.student.get_short_name(),
            self.score
        )

        return obj

    class Meta:
        verbose_name = _('Pair Review Submission')
        verbose_name_plural = _('Pair Review Submissions')
        ordering = ['user', 'student', 'created_at']
