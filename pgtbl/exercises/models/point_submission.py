from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from groups.models import Group
from modules.models import TBLSession


class GamificationPointSubmission(models.Model):
    """
    Store all point submissions for a given exercises question.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name=_("TBL sessions"),
        related_name="point_submissions"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Students'),
        related_name="point_submissions"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_('Groups'),
        related_name="point_submissions"
    )

    total_score = models.IntegerField(
        _("Total Score"),
        default=0,
        help_text=_("Student total score answered."),
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the submission of question is created."),
        auto_now_add=True
    )

    def __str__(self):
        """
        Alternative of question string.
        """

        obj = "{0}: {1}".format(
            self.student.get_short_name(),
            self.total_score
        )

        return obj

    class Meta:
        verbose_name = _('Gamification Point Submission')
        verbose_name_plural = _('Gamification Point Submissions')
        ordering = ['student', 'total_score', 'created_at']
