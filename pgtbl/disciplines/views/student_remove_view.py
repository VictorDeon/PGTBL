from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import DeleteView
from django.contrib import messages

from core.permissions import PermissionMixin
from disciplines.models import Discipline

# Get the custom user from settings
User = get_user_model()


class StudentRemoveView(LoginRequiredMixin,
                        PermissionMixin,
                        DeleteView):
    """
    Remove student from discipline.
    """

    template_name = 'students/list.html'
    permissions_required = [
        'show_discipline_permission'
    ]

    def get_object(self):
        """
        Get discipline by url slug
        """

        discipline = get_object_or_404(
            Discipline,
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def delete(self, request, *args, **kwargs):
        """
        Redirect to success url after remove the specific student
        from discipline.
        """

        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk', '')
        )

        discipline = self.get_object()

        is_logged_user = (self.request.user.id == user.id)
        is_teacher = (self.request.user.id == discipline.teacher.id)

        if is_logged_user or is_teacher:
            success_url = self.remove_from_discipline(user, is_teacher)
            return redirect(success_url)

        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': discipline.slug}
        )

        messages.error(
            self.request,
            _("You can't remove {0} from {1}"
              .format(user.get_short_name(), discipline.title))
        )

        return redirect(redirect_url)

    def remove_from_discipline(self, user, is_teacher=True):
        """
        Remove user from discipline.
        """

        discipline = self.get_object()

        if user in discipline.students.all():
            discipline.students.remove(user)

            if discipline.is_closed:
                discipline.is_closed = False
                discipline.save()
        else:
            discipline.monitors.remove(user)

        if is_teacher:
            messages.success(
                self.request,
                _("You have removed {0} from {1}"
                  .format(user.get_short_name(), discipline.title))
            )

            success_url = reverse_lazy(
                'disciplines:students',
                kwargs={'slug': discipline.slug}
            )
        else:
            messages.success(
                self.request,
                _("You left the discipline {0}"
                  .format(discipline.title))
            )

            success_url = reverse_lazy('accounts:profile')

        return success_url
