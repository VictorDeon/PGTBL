from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.forms import TopicForm
from forum.models import Topic
from notification.models import Notification


class TopicCreateView(LoginRequiredMixin,
                      PermissionMixin,
                      CreateView):
    """
    View to create a new topic inside forum.
    """

    model = Topic
    template_name = 'forum/form.html'
    form_class = TopicForm
    permissions_required = ['show_forum']

    def get_discipline(self):
        """
        Take the discipline that the forum belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert some attributes into forum context data.
        """

        context = super(TopicCreateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context

    def form_valid(self, form):
        """
        Receive the form already validated to create a topic.
        """

        form.instance.author = self.request.user
        form.instance.discipline = self.get_discipline()
        form.save()

        discipline = self.get_discipline()

        for student in discipline.students.all():
            if student != self.request.user:
                Notification.objects.create(
                    title=_("Topic created"),
                    description=_("Topic {0} created".format(form.instance.title)),
                    sender=self.request.user,
                    receiver=student,
                    discipline=discipline
                )

        for monitor in discipline.monitors.all():
            if monitor != self.request.user:
                Notification.objects.create(
                    title=_("Topic created"),
                    description=_("Topic {0} created".format(form.instance.title)),
                    sender=self.request.user,
                    receiver=monitor,
                    discipline=discipline
                )

        if discipline.teacher != self.request.user:
            Notification.objects.create(
                title=_("Topic created"),
                description=_("Topic {0} created".format(form.instance.title)),
                sender=self.request.user,
                receiver=discipline.teacher,
                discipline=discipline
            )

        messages.success(self.request, _('Topic created successfully.'))

        return super(TopicCreateView, self).form_valid(form)

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

        success_url = reverse_lazy(
            'forum:list',
            kwargs={
                'slug': discipline.slug,
            }
        )

        return success_url