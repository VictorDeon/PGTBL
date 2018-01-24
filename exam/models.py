from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db import models

# App imports
from TBLSessions.models import TBLSession
from groups.models import Group

# External app imports
from markdown_deux import markdown


class Exam(models.Model):
    """
    Team Based Learning tests
    """

    score = models.PositiveIntegerField(
        _('Score'),
        default=0,
        help_text=_('Exam final score.')
    )

    datetime = models.DateTimeField(
        _('Provide the test'),
        help_text=_('Date and time to provide the test to be answered.')
    )

    time = models.PositiveIntegerField(
        _('Time to answer'),
        default=40,
        help_text=_('Time to answer the test in minutes.')
    )

    is_closed = models.BooleanField(
        _('Is closed?'),
        default=True,
        help_text=_("Verify if the test is closed, if open the students can \
                     see and answer the test.")
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the exam is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the exam is updated."),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')
        ordering = ['created_at']


class iRAT(Exam):
    """
    Individual Readiness assurance test.
    """

    tbl_session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        related_name='iRATs'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='iRATs'
    )

    def clone(self, student):
        """
        Creates a copy of the iRAT evaluation questions for use in the gRAT
        """

        test = iRAT(
            tbl_session=self.tbl_session,
            score=0,
            datetime=self.datetime,
            time=self.time,
            is_closed=self.is_closed
        )

        for question in test.questions:
            question.score = 0
            question.show_answer = False
            question.save()

        return self.questions

    def __str__(self):
        """
        Exam string.
        """

        if self.student:
            return "{0}: iRAT of session {1}".format(
                self.student.get_short_name(),
                self.tbl_session.title
            )

        return "iRAT of session {0}".format(self.tbl_session.title)

    class Meta:
        verbose_name = _('iRAT')
        verbose_name_plural = _('iRAT')
        ordering = ['created_at']


class gRAT(Exam):
    """
    Group Readiness assurance test.
    """

    tbl_session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        related_name='gRATs'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        related_name='gRATs'
    )

    def __str__(self):
        """
        Exam string.
        """

        if self.group:
            return "{0}: gRAT of session {1}".format(
                self.group.title,
                self.tbl_session.title
            )

        return "gRAT of session {1}".format(self.tbl_session.title)

    class Meta:
        verbose_name = _('gRAT')
        verbose_name_plural = _('gRAT')
        ordering = ['created_at']


class PracticalTest(models.Model):
    """
    Practical evaluation: Application of concepts.
    """

    session = models.OneToOneField(
        TBLSession,
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        _('Description'),
        help_text=_("Practical test description")
    )

    is_closed = models.BooleanField(
        _('Is closed?'),
        default=True,
        help_text=_("Verify if the test is closed, if open the students can \
                     see and answer the test.")
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the practical test is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the practical test is updated."),
        auto_now=True
    )

    def description_markdown(self):
        """
        Transform description in markdown and render in html with safe
        """

        content = self.description
        return mark_safe(markdown(content))

    class Meta:
        verbose_name = _('Practical test')
        verbose_name_plural = _('Practical test')
