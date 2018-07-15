from django.utils.translation import ugettext_lazy as _
from django.db import models
from modules.models import TBLSession


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
