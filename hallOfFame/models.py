from django.db import models
from django.core.validators import MinValueValidator

from disciplines.models import Discipline

import datetime

# def year_choices():
#     list = []
#     c = current_year()
#     list.append(c)
#     l = current_year() - 1
#     list.append(l)
#
#     return list
#
# def year_choices():
#     list = [(r,r) for r in range(current_year() - 1, datetime.date.today().year+1)]
#
#     return list
#
def current_year():
    return datetime.date.today().year
#
# def semester_choices():
#     list = [(r,r) for r in range(0, 3)]
#
#     return list

class HallOfFame(models.Model):

        discipline = models.OneToOneField(
            Discipline,
            on_delete=models.CASCADE,
            verbose_name='Discipline',
            related_name='hall'
        )

        year = models.IntegerField(
            'year',
            default=current_year
        )

        semester = models.IntegerField(default=0)
