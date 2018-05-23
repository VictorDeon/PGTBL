# Django app
from django.shortcuts import render
from django.views import generic
from django.contrib import messages

# App
from hallOfFame.models import HallOfFame
from disciplines.models import Discipline
from .form import HallOfFameForm

class CreateHallView(generic.CreateView):

    model = HallOfFame
    template_name = 'disciplines/close.html'
    form_class = HallOfFameForm
    # success_url = reverse_lazy('accounts:profile')

    # Permissions
    # failure_redirect_path = reverse_lazy('accounts:profile')
    # permissions_required = [
    #     'create_discipline'
    # ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline




    def form_valid(self, form):
        """
        Receive the form already validated to create a discipline.
        """

        # Specifies who is the creator of the discipline
        form.instance.teacher = self.request.user
        form.instance.discipline = self.get_discipline()

        # Save the instance to slugify
        form.save()

        # Autocomplete slug url with id-title-classroom
        # form.instance.slug = slugify(
        #     str(form.instance.id) +
        #     "-" +
        #     form.instance.title +
        #     "-" +
        #     form.instance.classroom
        # )

        # Save slug
        # form.save()

        # messages.success(self.request, _('Hall created successfully.'))

        # Redirect to success url
        return super(CreateHallView, self).form_valid(form)


class ShowHallView(generic.ListView):
    template_name = 'hallOfFame/hall.html'
    model = HallOfFame
    context_object_name = 'hall_of_fame'

    # Permissions
    permissions_required = [
        'show_discipline_groups_permission'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.kwargs.get('slug', '')}
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Take the discipline from slug
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowRankingGroupView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context
