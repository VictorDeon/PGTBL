from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from TBLSessions.models import TBLSession
from groups.models import Group


class Question(models.Model):
    """
    Create questions to insert into list of exercises and evaluations.
    """

    title = models.CharField(
        _('Title'),
        max_length=1000,
        help_text=_('Question title.')
    )

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    LEVELS = [
        (_('Basic'), _('Basic')),
        (_('Intermediary'), _('Intermediary')),
        (_('Advanced'), _('Advanced')),
    ]

    level = models.CharField(
        _('Level'),
        max_length=15,
        choices=LEVELS,
        default='basic',
        help_text=_('Difficulty level')
    )

    topic = models.CharField(
        _('Topic'),
        max_length=100,
        help_text=_('Question topic.')
    )

    is_exercise = models.BooleanField(
        _('Is it an exercise?'),
        default=True,
        help_text=_('Exercise are questions that appear in the exercise list.')
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the question is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the question is updated."),
        auto_now=True
    )

    def __str__(self):
        """
        Question string.
        """

        return self.title

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['title', 'created_at']


class Alternative(models.Model):
    """
    Question alternatives.
    """

    title = models.CharField(
        _('Title'),
        max_length=1000,
        help_text=_('Alternative title.')
    )

    is_correct = models.BooleanField(
        _('Is correct?'),
        default=False,
        help_text=_('Is correct alternative to answer the question.')
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='alternatives'
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the alternative of question is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the alternative of question is updated."),
        auto_now=True
    )

    def __str__(self):
        """
        Alternative of question string.
        """

        return self.title

    class Meta:
        verbose_name = _('Alternative')
        verbose_name_plural = _('Alternatives')
        ordering = ['title', 'created_at']


class Submission(models.Model):
    """
    Store all submissions for a given question.
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


class ExerciseSubmission(Submission):
    """
    Store all submissions for a given exercise question.
    """

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


class IRATSubmission(Submission):
    """
    Store all submissions for a given iRAT question.
    """

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
        verbose_name = _('iRAT Submission')
        verbose_name_plural = _('iRAT Submissions')
        ordering = ['user', 'question', 'created_at']


class GRATSubmission(Submission):
    """
    Store all submissions for a given gRAT question.
    """

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_('Groups'),
        related_name="submissions"
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
