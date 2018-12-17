from django.utils.translation import ugettext_lazy as _
from django.db import models
from .tag import Tag


class News(models.Model):
    """
    Informations about the software.
    """

    title = models.CharField(
        _('Title'),
        help_text=_("Title of information."),
        max_length=100
    )

    image = models.ImageField(
        upload_to='news',
        help_text=_('Image about information.'),
        verbose_name=_('Image'),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_('Date of creation of information'),
        auto_now_add=True
    )

    link = models.URLField(
        _('Link of information'),
        blank=True,
        null=True
    )

    content = models.TextField(_('Description'))

    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        related_query_name='tags',
        blank=True
    )

    slug = models.SlugField(
        _('Identify'),
        max_length=100
    )

    def __str__(self):
        """
        String format of object.
        """

        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('-created_at', 'title')
