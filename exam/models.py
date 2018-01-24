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

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name='exams'
    )

    score = models.PositiveIntegerField(
        _('Score'),
        default=0,
        help_text=_('Exam final score.')
    )

    datetime = models.DateTimeField(
        _('Provide the test'),
        help_text=_('Date and time to provide the test to be answered.')
    )

    time = models.TimeField(
        _('Time to answer.'),
        help_text=_("Time to answer the test."),
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

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name='iRATs'
    )

    def get_questions(self):
        """
        Creates a copy of the iRAT evaluation questions for use in the gRAT
        """

        for question in self.questions:
            question.score = 0
            question.show_answer = False

        return self.questions

    def __str__(self):
        """
        Exam string.
        """

        return "iRAT of session {0}".format(self.session.title)

    class Meta:
        verbose_name = _('iRAT')
        verbose_name_plural = _('iRAT')
        ordering = ['created_at']


class gRAT(Exam):
    """
    Group Readiness assurance test.
    """

    groups = models.ManyToManyField(
        Group,
        verbose_name='gRATs'
    )

    def __str__(self):
        """
        Exam string.
        """

        return "gRAT of session {0}".format(self.session.title)

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
