from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from forum.forms import TopicForm
from forum.models import Topic


class TopicUpdateView(LoginRequiredMixin,
                      PermissionMixin,
                      UpdateView):
    """
    View to update a specific topic.
    """

    model = Topic
    template_name = 'forum/form.html'
    context_object_name = 'topic'
    form_class = TopicForm

    permissions_required = []

    def get_discipline(self):
        """
        Take the discipline that the topic belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_object(self):
        """
        Get the specific topic from discipline.
        """

        topic = Topic.objects.get(
            discipline=self.get_discipline(),
            pk=self.kwargs.get('pk', '')
        )

        return topic

    def get_context_data(self, **kwargs):
        """
        Insert a discipline and session inside appeal form template.
        """


        context = super(TopicUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('Topic updated successfully.'))

        return super(TopicUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        topic = self.get_object()

        success_url = reverse_lazy(
            'forum:detail',
            kwargs={
                'slug': discipline.slug,
                'pk': topic.id
            }
        )

        return success_url