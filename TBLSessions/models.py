from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from disciplines.models import Discipline
from markdown_deux import markdown
from django.db import models


class TBLSession(models.Model):
    """
    Create TBL sessions.
    """

    discipline = models.ForeignKey(
        Discipline,
        verbose_name='Discipline',
        related_name='tbl_sessions'
    )

    title = models.CharField(
        _('Title'),
        max_length=200,
        help_text=_('Session title.')
    )

    description = models.TextField(
        _('Description'),
        help_text=_('TBL session description.')
    )

    is_closed = models.BooleanField(
        _("Is closed?"),
        default=False,
        help_text=_("Close TBL session.")
    )

    irat_datetime = models.DateTimeField(
        _("iRAT date"),
        blank=True,
        null=True,
        help_text=_("Date and time to provide the iRAT test.")
    )

    irat_duration = models.PositiveIntegerField(
        _("iRAT durantion in minutes"),
        default=30,
        help_text=_("iRAT duration in minutes to be answered.")
    )

    grat_available = models.BooleanField(
        _("Release the gRAT test"),
        default=False,
        help_text=_("Release the gRAT test to be answered.")
    )

    grat_duration = models.PositiveIntegerField(
        _("gRAT durantion in minutes"),
        default=30,
        help_text=_("gRAT duration in minutes to be answered.")
    )

    practical_available = models.BooleanField(
        _("Release the practical test"),
        default=False,
        help_text=_("Release the practical test.")
    )

    peer_review_available = models.BooleanField(
        _("Release the peer review test"),
        default=False,
        help_text=_("Release the peer review test to be answered.")
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the session is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the session is updated."),
        auto_now=True
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}'.format(self.title)

    def description_markdown(self):
        """
        Transform description in markdown and render in html with safe
        """

        content = self.description
        return mark_safe(markdown(content))

    class Meta:
        verbose_name = _('TBL Session')
        verbose_name_plural = _('TBL Sessions')
        ordering = ['title', 'created_at']
