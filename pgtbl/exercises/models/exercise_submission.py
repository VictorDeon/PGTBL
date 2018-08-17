from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from modules.models import TBLSession
from questions.models.question import Question


class ExerciseSubmission(models.Model):
    """
    Store all submissions for a given exercises question.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name=_("TBL sessions"),
        related_name="exercise_submissions"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Questions"),
        related_name="exercise_submissions"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Users'),
        related_name="exercise_submissions"
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
            self.user.get_short_name(),
            self.question,
            self.score
        )

        return obj

    class Meta:
        verbose_name = _('Exercise Submission')
        verbose_name_plural = _('Exercise Submissions')
        ordering = ['user', 'question', 'created_at']
