from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from exercises.forms.exercise_form import ExerciseForm
from modules.models import TBLSession


class ExerciseUpdateView(LoginRequiredMixin,
                         PermissionMixin,
                         UpdateView):
    """
    Update the exercise gamification weight
    """

    model = TBLSession
    template_name = 'exercises/list.html'
    form_class = ExerciseForm

    # Permissions
    permissions_required = ['only_edit_by_teacher']

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('Exercise gamification weight updated successfully.'))

        return super(ExerciseUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'exercises:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url