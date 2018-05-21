# Django app
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from hallOfFame.models import HallOfFame


class ShowHallView(generic.ListView):
    template_name = 'hallOfFame/hall.html'
    model = HallOfFame
