from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from markdown_deux import markdown
from taggit.managers import TaggableManager

from disciplines.models import Discipline


class Topic(models.Model):
    """
    Forum topic view.
    """

    title = models.CharField(
        _('Title'),
        max_length=100,
        help_text=_('Topic title')
    )

    content = models.TextField(
        _('Content'),
        help_text=_('Topic forum content')
    )

    tags = TaggableManager()

    views = models.IntegerField(
        _("User views count"),
        blank=True,
        default=0
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
        related_name='topics'
    )

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='topics'
    )

    qtd_answers = models.IntegerField(
        _("Answer Count"),
        blank=True,
        default=0
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the topic is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the topic is updated."),
        auto_now=True
    )

    def __str__(self):
        """
        Topic string.
        """

        return self.title

    @property
    def tag(self):
        """
        Get all tags by string
        """

        return ", ".join(o.name for o in self.tags.all())

    def content_markdown(self):
        """
        Transform description in markdown and render in html with safe
        """

        content = self.content
        return mark_safe(markdown(content))

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['-updated_at']