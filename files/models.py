from django.utils.translation import ugettext_lazy as _
from django.db import models

# App imports
from disciplines.models import Discipline
from TBLSessions.models import TBLSession


class File(models.Model):
    """
    Insert files to discipline.
    """

    title = models.CharField(
        _('Title'),
        max_length=200,
        help_text=_('Title of file.')
    )

    description = models.TextField(
        _('Description'),
        max_length=500,
        help_text=_('Description of file.')
    )

    extension = models.CharField(
        _('File extension'),
        max_length=10,
        help_text=_('File extension.')
    )

    archive = models.FileField(
        _('File'),
        upload_to='disciplines/files',
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the file is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Date that the file is updated"),
        auto_now=True
    )

    def get_title(self):
        """
        Get the title by snakecase format.
        """

        new_title = ""

        for letter in self.title:
            if letter == ' ':
                letter = '_'

            new_title += letter

        return new_title.lower()

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return self.title

    class Meta:
        """
        Class metadata.
        """

        verbose_name = _("File")
        verbose_name_plural = _("Files")
        ordering = ['title', 'created_at']


class DisciplineFile(File):
    """
    Insert files into discipline.
    """

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='files'
    )


class SessionFile(File):
    """
    File to insert into tbl sessions.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name='Session',
        related_name='files'
    )
