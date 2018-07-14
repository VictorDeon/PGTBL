from django.utils.translation import ugettext_lazy as _
from django.db import models
from .question import Question


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
