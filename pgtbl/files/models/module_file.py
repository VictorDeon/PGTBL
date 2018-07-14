from django.db import models
from TBLSessions.models import TBLSession
from .file import File


class ModuleFile(File):
    """
    File to insert into tbl sessions.
    """

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name='Session',
        related_name='files'
    )
