# Django
from django.core.validators import MinValueValidator
from django.db import models

# App
from disciplines.models import Discipline
from groups.models import Group

class Ranking(models.Model):

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='ranking'
    )


class GroupInfo(models.Model):

    ranking = models.ForeignKey(
        Ranking,
        related_name="groups_info"
    )

    group = models.OneToOneField(
        Group,
        related_name="group_info"
    )

    results = models.FloatField(
        verbose_name="results",
        default=0.0,
        help_text="results of group info."
    )
