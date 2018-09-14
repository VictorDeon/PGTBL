from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from disciplines.models import Discipline

User = get_user_model()


class HallOfFameGroup(models.Model):
    """
    Create hall of fame group.
    """

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='hall_of_fame',
    )

    title = models.CharField(
        _('Title'),
        max_length=50,
        blank=True,
        help_text=_('Title of group')
    )

    students = models.ManyToManyField(
        User,
        verbose_name='Students',
        related_name='hall_of_fame',
        blank=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the group is created."),
        auto_now_add=True
    )

    def get_semester(self):
        """
        By created at get the discipline semester.
        """

        if self.created_at.month < 8:
            return 1

        return 2

    def get_year(self):
        """
        By created at get the discipline year.
        """

        return self.created_at.year

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return self.title

    class Meta:
        verbose_name = _("Hall of Fame Groups")
        verbose_name_plural = _("Hall of Fame Groups")
        ordering = ['title', 'created_at']