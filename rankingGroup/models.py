from django.db import models

# App imports
from disciplines.models import Discipline
from groups.models import Group
from TBLSessions.models import TBLSession

class RankingGroup(models.Model):

    """
    Create RankingGroup.
    """
    #RankingGroup

    # discipline = models.ForeignKey(
    #     Discipline,
    #     on_delete=models.CASCADE,
    #     verbose_name='Ranking',
    #     related_name='ranking_group'
    # )

    session = models.ForeignKey(
        TBLSession,
        on_delete=models.CASCADE,
        verbose_name='Ranking',
        related_name='ranking_group'
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        related_name='groups_class',
        blank=True
    )
