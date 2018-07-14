from django.utils.translation import ugettext_lazy as _
from django.db import models


class Submission(models.Model):
    """
    Store all submissions for a given question.
    """

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

    class Meta:
        abstract = True
