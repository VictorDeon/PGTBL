from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms

import datetime

# App imports
from pagedown.widgets import PagedownWidget
from .models import HallOfFame

def year_choices():
    list = [(r,r) for r in range(current_year() - 1, datetime.date.today().year+1)]

    return list

def current_year():
    return datetime.date.today().year

def semester_choices(): 
    list = [(r,r) for r in range(0, 3)]

    return list

YEARS = year_choices()

class HallOfFameForm(forms.ModelForm):
    """
    Form to create a new HallOfFameForm.
    """

    class Meta:
        model = HallOfFame
        fields = [
            'year','semester',
        ]

    year = forms.ChoiceField(label='year', choices=YEARS)

    semester = forms.ChoiceField(label='semester', choices=((0,0),(1,1),(2,2)))
