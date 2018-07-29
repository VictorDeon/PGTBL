from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from groups.models import Group
from modules.models import TBLSession
from questions.models.question import Question


class GRATSubmission(models.Model):
    """
    Store all submissions for a given gRAT question.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name=_("TBL sessions"),
        related_name="grat_submissions"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Questions"),
        related_name="grat_submissions"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Users'),
        related_name="grat_submissions"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_('Groups'),
        related_name="submissions"
    )

    correct_alternative = models.CharField(
        _('Correct Alternative'),
        max_length=1000,
        help_text=_('Correct alternative title.')
    )

    score = models.PositiveIntegerField(
        _("Score"),
        default=0,
        help_text=_("Question score answered."),
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

        obj = "{0}: {1} - {2}".format(
            self.group.title,
            self.question,
            self.score
        )

        return obj

    class Meta:
        verbose_name = _('gRAT Submission')
        verbose_name_plural = _('gRAT Submissions')
        ordering = ['group', 'question', 'created_at']
