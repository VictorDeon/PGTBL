# Django app
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy


# App
from hallOfFame.models import HallOfFame
from disciplines.models import Discipline
from .form import HallOfFameForm

import datetime


class CreateHallView(generic.CreateView):

    model = HallOfFame
    template_name = 'hallOfFame/close.html'
    form_class = HallOfFameForm
    context_object_name = "hall"
    success_url = reverse_lazy('discipline:details')



    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline



    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.discipline = self.get_discipline()
        self.object = form.save()

        print(self.object)

        messages.success(self.request, _('TBL session created successfully.'))

        return super(CreateHallView,self).form_valid(form)


    def form_invalid(self, form):
        """
        Redirect to form with form errors.
        """

        messages.error(
            self.request,
            ("Invalid fields, please fill in the fields correctly.")
        )


    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'discipline:deta',
            kwargs={'slug': discipline.slug}
        )

        return success_url


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """
        current = datetime.date.today().year

        last = current -1

        context = super(CreateHallView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()

        return context


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
