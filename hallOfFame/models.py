from django.db import models
from django.core.validators import MinValueValidator
from disciplines.models import Discipline

from rankingGroup.models import GroupInfo

import datetime

def current_year():
    return datetime.date.today().year


class HallOfFame(models.Model):

        group_info = models.ForeignKey(
            GroupInfo,
            related_name="hall",
            default=False
        )

        discipline = models.ForeignKey(
            Discipline,
            related_name="halls"

        )

        year = models.IntegerField(
            'year',
            default=current_year
        )

        semester = models.IntegerField(default=0)
