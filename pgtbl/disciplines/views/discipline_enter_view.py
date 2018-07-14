from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

from disciplines.forms import DisciplineEnterForm
from disciplines.models import Discipline


class DisciplineEnterView(LoginRequiredMixin, FormView):
    """
    Insert students or monitors inside discipline.
    """

    form_class = DisciplineEnterForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'disciplines/list.html'

    def form_valid(self, form):
        """
        Form to insert students and monitors in the discipline.
        """

        success = self.enter_discipline(form)

        if success:
            # Redirect to success_url
            return super(DisciplineEnterView, self).form_valid(form)

        # Redirect to same page with error.
        redirect_url = reverse_lazy('disciplines:search')

        return redirect(redirect_url)

    def enter_discipline(self, form):
        """
        Verify if the password is correct and insert user in the discipline.
        """

        try:
            discipline = Discipline.objects.get(
                Q(password=form.cleaned_data['password']),
                Q(slug=self.kwargs.get('slug', ''))
            )
        except Exception:
            messages.error(
                self.request,
                _("Incorrect Password.")
            )

            return False

        if discipline.is_closed:
            messages.error(
                self.request,
                _("Discipline is closed.")
            )

            return False

        if self.request.user.is_teacher:
            success = self.insert_monitor(discipline)
        else:
            success = self.insert_student(discipline)

        if success:
            messages.success(
                self.request,
                _("You have been entered into the discipline: {0}"
                  .format(discipline.title))
            )

            return True

        return False

    def insert_monitor(self, discipline):
        """
        If user is a teacher, he will have all permission of monitor
        If monitor number is bigger than monitors limit, can't enter.
        """

        if discipline.monitors.count() >= discipline.monitors_limit:
            messages.error(
                self.request,
                _("There are no more vacancies to monitor")
            )

            return False

        if self.request.user.id == discipline.teacher.id:
            messages.error(
                self.request,
                _("You can't get into your own discipline.")
            )

            return False

        discipline.monitors.add(self.request.user)

        return True

    def insert_student(self, discipline):
        """
        If user is a student, he will have all permission of student
        If students number is bigger than student limit of discipline, close it
        """

        if discipline.students.count() >= discipline.students_limit:
            if not discipline.is_closed:
                discipline.is_closed = True
                discipline.save()

            messages.error(
                self.request,
                _("Crowded discipline.")
            )

            return False

        discipline.students.add(self.request.user)

        return True
