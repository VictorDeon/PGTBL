from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from disciplines.models import Discipline


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

    final_grade = models.FloatField(
        _("Final grade"),
        default=0.0,
        help_text=_("Student final grade.")
    )

    status = models.CharField(
        _('Status'),
        max_length=15,
        default=_('Disapproved'),
        help_text=_('Student status')
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

        grade = 0.0
        if number_of_sessions > 0:
            grade = (session_grades / number_of_sessions)

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
