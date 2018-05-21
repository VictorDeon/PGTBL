from django.db import models
from disciplines.models import Discipline
# Create your models here.

class HallOfFame(models.Model):

        discipline = models.OneToOneField(
            Discipline,
            on_delete=models.CASCADE,
            verbose_name='Discipline',
            related_name='hall'
        )
