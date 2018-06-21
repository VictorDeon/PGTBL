# Django app
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


# App
from hallOfFame.models import HallOfFame
from disciplines.models import Discipline
from rankingGroup.models import Ranking, GroupInfo
from .form import HallOfFameForm
from TBLSessions.models import TBLSession

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
                ("There are no groups available to create a rank")
            )

        return first_groupInfo

    def search_disciplines(self):
        """
        Search from disciplines a specific discipline.
        """
        query = self.request.GET.get("q_info")

        return query


    def get_hallOfFame(self):
        """
        Get the info_group queryset from model database.
        """

        year = self.search_disciplines()
        discipline = self.get_discipline()
        halls = HallOfFame.objects.filter(discipline=discipline).order_by('-year', '-semester')


        return halls
    
    def get_sessions_open(self):
        """
        Get the closeds tbl sessions from model database.
        """

        discipline = self.get_discipline()
        sessions =  TBLSession.objects.filter(discipline=discipline,is_closed=False)

        return sessions

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        form.instance.discipline = self.get_discipline()
        form.instance.group_info = self.get_groupsInfo()
        # self.object = form.save()

        sessions = self.get_sessions_open()
        halls = self.get_hallOfFame()

        discipline = self.get_discipline()

        semester = form.cleaned_data.get('semester')
        year = form.cleaned_data.get('year')

        if(len(halls.filter(discipline=discipline, year=year, semester=semester)) == 0 and len(sessions) == 0):
            messages.success(self.request,  ('Hall of Fame added successfully.'))
            discipline.is_closed = True
            discipline.save()
            return super(CreateHallView,self).form_valid(form)
        elif(len(sessions) != 0):
            messages.error(self.request,  ('Hall of Fame not added. All sessions must be closed.'))
            return redirect(self.get_success_url())
        elif(len(halls.filter(discipline=discipline, year=year, semester=semester)) != 0):
            messages.error(self.request,  ('Hall of Fame not added. Hall of Fame for this year and semester already exist.'))
            return redirect(self.get_success_url())
        else:
            messages.error(self.request,  ('Hall of Fame not added.'))
            return redirect(self.get_success_url())

 


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
    
    def search_disciplines(self):
        """
        Search from disciplines a specific discipline.
        """
        query = self.request.GET.get("q_info")

        return query




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

        year = self.search_disciplines()
        discipline = self.get_discipline()
        if(year):
            halls = HallOfFame.objects.filter(discipline=discipline, year=year).order_by('-year', '-semester')
        else:
            halls = HallOfFame.objects.filter(discipline=discipline).order_by('-year', '-semester')


        return halls
