from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class DisciplineManager(models.Manager):
    """
    Create a custom search discipline queryset.
    """

    def search(self, query):
        """
        Search a discipline by name or description
        """

        return self.get_queryset().filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)
        )


class Discipline(models.Model):
    """
    Create a discipline model.
    """

    title = models.CharField(
        _('Title'),
        max_length=100,
        help_text=_("Discipline title")
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_("Discipline description")
    )

    course = models.CharField(
        _('Course'),
        max_length=100,
        blank=True,
        help_text=_("Discipline course")
    )

    # url shortcut
    slug = models.SlugField(
        _('Shortcut')
    )

    # Teacher that create disciplines.
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Teacher'),
        related_name="disciplines"
    )

    # Create a date when the user is created
    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the discipline is created."),
        auto_now_add=True
    )

    # Create or update the date after the user is updated
    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the discipline is updated."),
        auto_now=True
    )

    # Insert new queryset into the model
    objects = DisciplineManager()

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0} - {1}'.format(self.title, self.course)

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _('Disciplines')
        ordering = ['title', 'created_at']
