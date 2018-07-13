from django.utils.translation import ugettext_lazy as _
from django.db import models


class Tag(models.Model):
    """
    Tags for improve system features.
    """

    title = models.CharField(
        _('Tag'),
        max_length=20
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
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
