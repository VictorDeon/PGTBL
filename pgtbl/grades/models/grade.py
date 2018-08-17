from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from modules.models import TBLSession
from groups.models import Group


class Grade(models.Model):
    """
    Student TBL Session grade.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name='TBL Session',
        related_name='grades'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Students',
        related_name='session_grades'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
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
            self.student.get_short_name(),
            self.calcule_session_grade()
        )

    class Meta:
        verbose_name = _('TBL Session grades')
        verbose_name_plural = _('TBL Sessions grades')
        ordering = ['session', 'student', 'created_at']
