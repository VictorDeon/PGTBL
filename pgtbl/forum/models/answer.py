from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from forum.models import Topic


class Answer(models.Model):
    """
    Answer
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
        related_name='answers'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name=_('Topic'),
        related_name='answers'
    )

    content = models.TextField(
        _('Content'),
        help_text=_('Answer topic content')
    )

    is_correct = models.BooleanField(
        _("Is correct?"),
        blank=True,
        default=False
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the answer is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the answer is updated."),
        auto_now=True
    )

    def __str__(self):
        """
        Topic string.
        """

        return self.content[:100]

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        ordering = ['-is_correct', 'created_at']