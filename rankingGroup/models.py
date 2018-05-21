# Django
from django.db import models
from django.core.validators import MinValueValidator

# App
from disciplines.models import Discipline
from groups.models import Group

class GroupInfo(models.Model):

    position = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    group = models.ManyToManyField(
        Group,
    )

    results = models.FloatField(
        default=0.0,
    )


class Ranking(models.Model):

    discipline = models.OneToOneField(
        Discipline
    )

    group_info = models.ManyToManyField(
        GroupInfo
    )
