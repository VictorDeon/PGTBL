from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from TBLSessions.models import TBLSession
from .question import Question
from .submission import Submission


class ExerciseSubmission(Submission):
    """
    Store all submissions for a given exercise question.
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
