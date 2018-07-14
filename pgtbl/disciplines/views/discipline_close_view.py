from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView
from django.shortcuts import redirect

from core.permissions import PermissionMixin
from disciplines.models import Discipline


class DisciplineCloseView(LoginRequiredMixin,
                          PermissionMixin,
                          DeleteView):

    model = Discipline
    template_name = 'disciplines/details.html'
    permissions_required = [
        'show_discipline_permission',
        'change_own_discipline'
    ]

    def delete(self, request, *args, **kwargs):
        """
        Close or open discipline.
        """

        discipline = self.get_object()

        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': discipline.slug}
        )

        if discipline.is_closed:
            discipline.is_closed = False
        else:
            discipline.is_closed = True

        discipline.save()

        return redirect(redirect_url)
