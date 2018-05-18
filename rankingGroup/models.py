from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from disciplines.models import Discipline
from groups.models import Group



class Ranking(models.Model):

    """
    Ranking of groups Session grade.
    """


    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='TBL discipline',
        related_name='rankig',
        null=False,
        default=-1
    )

    group = models.ManyToManyField(
        Group,
        related_name='ranking'
    )
    sum_results_sessions = models.FloatField(
        _("sum results for group"),
        default=0.0,
        help_text=_("sum results for group")
    )
