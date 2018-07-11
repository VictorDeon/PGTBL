from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

# App imports
from disciplines.models import Discipline

User = get_user_model()


class Group(models.Model):
    """
    Create groups to TBL.
    """

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='groups',
    )

    title = models.CharField(
        _('Title'),
        max_length=50,
        help_text=_('Title of group')
    )

    students_limit = models.PositiveIntegerField(
        _('Students limit'),
        default=0,
        help_text=_("Students limit to get into the group.")
    )

    students = models.ManyToManyField(
        User,
        verbose_name='Students',
        related_name='student_groups',
        blank=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the group is created."),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Date that the group is updated"),
        auto_now=True
    )

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return self.title

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ['title', 'created_at']
