from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db import models
from disciplines.models import Discipline
from groups.models import Group
from markdown_deux import markdown


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

    irat_weight = models.PositiveIntegerField(
        _("iRAT weight"),
        default=3,
        help_text=_("iRAT test weight.")
    )

    irat_duration = models.PositiveIntegerField(
        _("iRAT durantion in minutes"),
        default=30,
        help_text=_("iRAT duration in minutes to be answered.")
    )

    grat_datetime = models.DateTimeField(
        _("gRAT date"),
        blank=True,
        null=True,
        help_text=_("Date and time to provide the gRAT test.")
    )

    grat_weight = models.PositiveIntegerField(
        _("gRAT test weight"),
        default=2,
        help_text=_("gRAT test weight.")
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

    practical_weight = models.PositiveIntegerField(
        _("Practical test weight"),
        default=4,
        help_text=_("Practical test weight.")
    )

    peer_review_available = models.BooleanField(
        _("Release the peer review test"),
        default=False,
        help_text=_("Release the peer review test to be answered.")
    )

    peer_review_weight = models.PositiveIntegerField(
        _("Peer review weight"),
        default=1,
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

    class Meta:
        verbose_name = _('TBL Session')
        verbose_name_plural = _('TBL Sessions')
        ordering = ['title', 'created_at']


class Grade(models.Model):
    """
    Student grade.
    """

    session = models.ForeignKey(
        TBLSession,
        verbose_name='TBL Session',
        related_name='grades'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='User',
        related_name='grades'
    )

    group = models.ForeignKey(
        Group,
        verbose_name='Group',
        related_name='grades'
    )

    irat = models.FloatField(
        _("iRAT grade"),
        default=0.0,
        help_text=_("iRAT test grade.")
    )

    grat = models.FloatField(
        _("gRAT grade"),
        default=0.0,
        help_text=_("gRAT test grade.")
    )

    practical = models.FloatField(
        _("Practical test grade"),
        default=0.0,
        help_text=_("Practical test grade.")
    )

    peer_review = models.FloatField(
        _("Peer review grade"),
        default=0.0,
        help_text=_("Peer review grade.")
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

    def calcule_session_grade(self):
        """
        Calcule the session grade with iRAT, gRAT practical and peer review
        """

        session_grade = 0

        if self.session.peer_review_available:
            session_grade += (
                (self.irat * self.session.irat_weight) +
                (self.grat * self.session.grat_weight) +
                (self.practical * self.session.practical_weight)
            )

            session_grade /= (
                self.session.irat_weight +
                self.session.grat_weight +
                self.session.practical_weight
            )
        else:
            session_grade += (
                (self.irat * self.session.irat_weight) +
                (self.grat * self.session.grat_weight) +
                (self.practical * self.session.practical_weight) +
                (self.peer_review * self.session.peer_review_weight)
            )

            session_grade /= (
                self.session.irat_weight +
                self.session.grat_weight +
                self.session.practical_weight +
                self.session.peer_review_weight
            )

        return session_grade

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}: {1} - {2}'.format(
            self.session,
            self.user,
            self.session_score
        )

    class Meta:
        verbose_name = _('TBL Session grades')
        verbose_name_plural = _('TBL Sessions grades')
        ordering = ['session', 'user', 'created_at']
