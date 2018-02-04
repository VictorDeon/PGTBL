from django.utils.translation import ugettext_lazy as _
from django.conf import settings
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
        related_name='questions'
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

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Users'),
        related_name="submissions"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Questions"),
        related_name="submissions"
    )

    correct_alternative = models.CharField(
        _('Correct Alternative'),
        max_length=1000,
        help_text=_('Correct alternative title.')
    )

    EXAMS = (
        ('iRAT', 'iRAT'),
        ('gRAT', 'gRAT'),
        ('Exercise', 'Exercise')
    )

    exam = models.CharField(
        max_length=10,
        choices=EXAMS,
        default='Exercise'
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
            self.exam,
            self.question
        )

        return obj

    class Meta:
        verbose_name = _('Submission')
        verbose_name_plural = _('Submissions')
        ordering = ['user', 'exam', 'question', 'created_at']
