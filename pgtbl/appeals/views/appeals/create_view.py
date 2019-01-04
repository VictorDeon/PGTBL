from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from appeals.models import Appeal
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession
from appeals.forms import AppealForm
from modules.utils import get_datetimes
from notification.models import Notification


class AppealCreateView(LoginRequiredMixin,
                       PermissionMixin,
                       CreateView):
    """
    View to create a new appeal
    """

    model = Appeal
    template_name = 'appeals/form.html'
    form_class = AppealForm
    permissions_required = ['create_appeal']

    def get_discipline(self):
        """
        Take the discipline that the appeal belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the appeal belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('session_id', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert some attributes into appeal context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(AppealCreateView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        return context

    def form_valid(self, form):
        """
        Receive the form already validated to create a appeal.
        """

        form.instance.session = self.get_session()
        form.instance.student = self.request.user
        form.instance.group = self.get_student_group()
        form.save()

        self.send_notification(form)

        messages.success(self.request, _('Appeal created successfully.'))

        return super(AppealCreateView, self).form_valid(form)

    def send_notification(self, form):
        """
        Send notification to all monitors and teacher
        """

        discipline = self.get_discipline()

        for monitor in discipline.monitors.all():
            Notification.objects.create(
                title=_("Appeal Created"),
                description=_("Appeal {0} created by group {1}".format(form.instance.title, self.get_student_group())),
                sender=self.request.user,
                receiver=monitor,
                discipline=discipline
            )

        Notification.objects.create(
            title=_("Appeal Created"),
            description=_("Appeal {0} created by group {1}".format(form.instance.title, self.get_student_group())),
            sender=self.request.user,
            receiver=discipline.teacher,
            discipline=discipline
        )

    def form_invalid(self, form):
        """
        Redirect to form with form error.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the fields correctly.")
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'appeals:list',
            kwargs={
                'slug': discipline.slug,
                'session_id': session.id
            }
        )

        return success_url

    def get_student_group(self):
        """
        Get current student group.
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if self.request.user in group.students.all():
                return group