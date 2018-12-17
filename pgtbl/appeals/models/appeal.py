from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.db import models
from markdown_deux import markdown

from groups.models import Group
from modules.models import TBLSession
from questions.models import Question


class Appeal(models.Model):
    """
    Create appeals
    """

    title = models.CharField(
        _('Title'),
        max_length=100,
        help_text=_('Appeal title')
    )

    description = models.TextField(
        _('Description'),
        help_text=_('Appeal description')
    )

    is_accept = models.BooleanField(
        _('Is the appeals accept?'),
        default=False,
        help_text=_('If the appeals make sense this need to be accept.')
    )

    qtd_comments = models.IntegerField(
        _("Qtd Comments"),
        default=0,
        blank=True,
        help_text=_("Comment quantity")
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="appeals"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Student'),
        related_name='appeals'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Group',
        related_name='appeals'
    )

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name='TBL Session',
        related_name='appeals'
    )

    # Create a date when the discipline is created
    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the appeals is created."),
        auto_now_add=True
    )

    # Create or update the date after the discipline is updated
    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the appeals is updated."),
        auto_now=True
    )

    def __str__(self):
        """
        Appeal string.
        """

        return "{0}: {1}".format(self.title, self.question.title)

    def description_markdown(self):
        """
        Transform description in markdown and render in html with safe
        """

        content = self.description
        return mark_safe(markdown(content))

    class Meta:
        verbose_name = _('Appeal')
        verbose_name_plural = _('Appeals')
        ordering = ['title', 'created_at']