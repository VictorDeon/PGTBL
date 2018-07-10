from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db import models

# App imports
from disciplines.models import Discipline
from markdown_deux import markdown

class TBLSession(models.Model):
    """
    Create TBL sessions.
    """

    # TBL Session
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
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

    # iRAT test
    irat_datetime = models.DateTimeField(
        _("iRAT date"),
        blank=True,
        null=True,
        help_text=_("Date and time to provide the iRAT test.")
    )

    irat_weight = models.PositiveIntegerField(
        _("iRAT weight"),
        default=3,
        blank=True,
        help_text=_("iRAT test weight.")
    )

    irat_duration = models.PositiveIntegerField(
        _("iRAT durantion in minutes"),
        default=30,
        blank=True,
        help_text=_("iRAT duration in minutes to be answered.")
    )

    # gRAT test
    grat_datetime = models.DateTimeField(
        _("gRAT date"),
        blank=True,
        null=True,
        help_text=_("Date and time to provide the gRAT test.")
    )

    grat_weight = models.PositiveIntegerField(
        _("gRAT test weight"),
        default=2,
        blank=True,
        help_text=_("gRAT test weight.")
    )

    grat_duration = models.PositiveIntegerField(
        _("gRAT durantion in minutes"),
        default=30,
        blank=True,
        help_text=_("gRAT duration in minutes to be answered.")
    )

    # Practical test
    practical_available = models.BooleanField(
        _("Release the practical test"),
        default=False,
        help_text=_("Release the practical test.")
    )

    practical_weight = models.PositiveIntegerField(
        _("Practical test weight"),
        default=4,
        blank=True,
        help_text=_("Practical test weight.")
    )

    practical_description = models.TextField(
        _('Description'),
        help_text=_('Practical test description.')
    )

    # Peer Review test
    peer_review_available = models.BooleanField(
        _("Release the peer review test"),
        default=False,
        help_text=_("Release the peer review test to be answered.")
    )

    peer_review_weight = models.PositiveIntegerField(
        _("Peer review weight"),
        default=1,
        blank=True,
        help_text=_("Peer review weight.")
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

    def practical_test_markdown(self):
        """
        Transform practical test description in markdown and
        render in html with safe
        """

        content = self.practical_description
        return mark_safe(markdown(content))

    class Meta:
        verbose_name = _('TBL Session')
        verbose_name_plural = _('TBL Sessions')
        ordering = ['title', 'created_at']
