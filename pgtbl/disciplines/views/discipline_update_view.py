from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils.text import slugify
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.forms import DisciplineUpdateForm
from disciplines.models import Discipline


class DisciplineUpdateView(LoginRequiredMixin,
                           PermissionMixin,
                           UpdateView):
    """
    View to update a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    form_class = DisciplineUpdateForm
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    failure_redirect_path = reverse_lazy('accounts:profile')
    permissions_required = [
        'change_own_discipline'
    ]

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # Autocomplete slug url with id-title-classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        discipline = Discipline.objects.get(slug=self.kwargs.get('slug', ''))

        modify_student_limit = (
            discipline.students_limit < form.instance.students_limit
        )

        if modify_student_limit and discipline.is_closed:
            form.instance.is_closed = False

        form.save()

        messages.success(self.request, _("Discipline updated successfully."))

        # Redirect to success_url.
        return super(DisciplineUpdateView, self).form_valid(form)
