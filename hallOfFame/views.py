# Django app
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy


# App
from hallOfFame.models import HallOfFame
from disciplines.models import Discipline
from rankingGroup.models import Ranking, GroupInfo
from .form import HallOfFameForm

import datetime


class CreateHallView(generic.CreateView):

    model = HallOfFame
    template_name = 'hallOfFame/close.html'
    form_class = HallOfFameForm
    context_object_name = "halls"

    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_ranking(self):

        discipline = self.get_discipline()
        ranking = Ranking()
        try:
            ranking = Ranking.objects.get(discipline=discipline)
        except Ranking.DoesNotExist:
            obj = Ranking(discipline=discipline)
            obj.save()

        return ranking



    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_groupsInfo(self):

        discipline = self.get_discipline()

        ranking = self.get_ranking()

        groups_info = []
        first_groupInfo = GroupInfo()

        try:
            all_groupsInfo = GroupInfo.objects.filter(ranking=ranking)
            list = all_groupsInfo.order_by('-results')
            first_groupInfo = list[0]

        except GroupInfo.DoesNotExist:
            messages.error(
                self.request,
                ("Não houve a instancia de um group_info para o hall.")
            )



        return first_groupInfo



    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        form.instance.discipline = self.get_discipline()
        form.instance.group_info = self.get_groupsInfo()
        self.object = form.save()

        discipline = self.get_discipline()

        discipline.is_closed = True
        discipline.save()

        print(self.object.year)
        print(self.object.semester)
        print(self.object.group_info)
        print(self.object.discipline)

        messages.success(self.request,  ('Discipline session created successfully.'))

        return super(CreateHallView,self).form_valid(form)


    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()

        success_url = reverse_lazy(
            'disciplines:details',
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

        context['group_info'] = self.get_groupsInfo()

        return context


class ShowHallView(generic.ListView):
    template_name = 'hallOfFame/list.html'
    model = HallOfFame
    context_object_name = 'hall_of_fame'

    # Permissions
    permissions_required = [
        'show_discipline_groups_permission',
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

    def get_ranking(self):

        discipline = self.get_discipline()
        ranking = Ranking()
        try:
            ranking = Ranking.objects.get(discipline=discipline)
        except Ranking.DoesNotExist:
            obj = Ranking(discipline=discipline)
            obj.save()

        return ranking


    def get_context_data(self, **kwargs):
        """
        Insert a form inside group list.
        """

        context = super(ShowHallView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['halls'] = self.get_queryset()

        return context



    def get_queryset(self):
        """
        Get the info_group queryset from model database.
        """

        discipline = self.get_discipline()

        halls = HallOfFame.objects.filter(discipline=discipline)

        print(halls)


        return halls
