from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

# App imports
from TBLSessions.models import TBLSession
from disciplines.models import Discipline
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
        verbose_name='Students',
        related_name='session_grades'
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

        if not self.session.peer_review_available:
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
            self.student.get_short_name(),
            self.calcule_session_grade()
        )

    class Meta:
        verbose_name = _('TBL Session grades')
        verbose_name_plural = _('TBL Sessions grades')
        ordering = ['session', 'student', 'created_at']


class FinalGrade(models.Model):
    """
    Store the student grade of discipline.
    """

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Disciplines',
        related_name='grades'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Students',
        related_name='discipline_grades'
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

    def calcule_final_grade(self):
        """
        Calcule the student final grade.
        """

        session_grades = 0.0

        number_of_sessions = self.discipline.tbl_sessions.count()

        for session in self.discipline.tbl_sessions.all():
            for grade in session.grades.filter(student=self.student):
                session_grades += grade.calcule_session_grade()

        grade = (session_grades/number_of_sessions)

        return grade

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}: {1} - {2}'.format(
            self.discipline.title,
            self.student.get_short_name(),
            self.calcule_final_grade()
        )

    class Meta:
        verbose_name = _('Discipline grades')
        verbose_name_plural = _('Discipline grades')
        ordering = ['discipline', 'student', 'created_at']
