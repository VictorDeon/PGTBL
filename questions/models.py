from django.utils.translation import ugettext_lazy as _
from TBLSessions.models import TBLSession
from django.db import models


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
        verbose_name='questions'
    )

    LEVELS = {
        (_('Basic'), _('Basic')),
        (_('Intermediary'), _('Intermediary')),
        (_('Advanced'), _('Advanced')),
    }

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

    score = models.PositiveIntegerField(
        _('Score'),
        default=0,
        help_text=_('Question score.')
    )

    is_exercise = models.BooleanField(
        _('Is it an exercise?'),
        default=True,
        help_text=_('Exercise are questions that appear in the exercise list.')
    )

    show_answer = models.BooleanField(
        _('Show question answer.'),
        default=False,
        help_text=_('Show answer about the specific question')
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

    alternative_title = models.CharField(
        _('Title'),
        max_length=1000,
        help_text=_('Alternative title.')
    )

    SCORES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    )

    score = models.PositiveIntegerField(
        _('Score'),
        choices=SCORES,
        default=0,
        help_text=_('Alternative score.')
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

        return self.alternative_title

    class Meta:
        verbose_name = _('Alternative')
        verbose_name_plural = _('Alternatives')
        ordering = ['alternative_title', 'created_at']
