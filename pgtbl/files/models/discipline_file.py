from django.db import models
from disciplines.models import Discipline
from .file import File


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
