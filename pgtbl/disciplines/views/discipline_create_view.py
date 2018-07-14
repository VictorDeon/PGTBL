from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.utils.text import slugify
from django.contrib import messages
from core.permissions import ModelPermissionMixin
from disciplines.forms import DisciplineForm
from disciplines.models import Discipline


class DisciplineCreateView(LoginRequiredMixin,
                           ModelPermissionMixin,
                           CreateView):
    """
    View to create a new discipline.
    """

    model = Discipline
    template_name = 'disciplines/form.html'
    form_class = DisciplineForm
    success_url = reverse_lazy('accounts:profile')

    # Permissions
    failure_redirect_path = reverse_lazy('accounts:profile')
    permissions_required = [
        'create_discipline'
    ]

    def form_valid(self, form):
        """
        Receive the form already validated to create a discipline.
        """

        # Specifies who is the creator of the discipline
        form.instance.teacher = self.request.user
        # Save the instance to slugify
        form.save()

        # Autocomplete slug url with id-title-classroom
        form.instance.slug = slugify(
            str(form.instance.id) +
            "-" +
            form.instance.title +
            "-" +
            form.instance.classroom
        )

        # Save slug
        form.save()

        messages.success(self.request, _('Discipline created successfully.'))

        # Redirect to success url
        return super(DisciplineCreateView, self).form_valid(form)
