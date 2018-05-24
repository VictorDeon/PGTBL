from django.db import models
from django.core.validators import MinValueValidator

from disciplines.models import Discipline

import datetime

def current_year():
    return datetime.date.today().year


class HallOfFame(models.Model):

        discipline = models.ForeignKey(
            Discipline,
            
        )

        year = models.IntegerField(
            'year',
            default=current_year
        )

        semester = models.IntegerField(default=0)
