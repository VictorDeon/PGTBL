from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter(name='change')
@stringfilter
def change(value, arg):
    """
    Scrolls through the string and changes some characters
    """

    chlist = arg.split()
    return value.replace(chlist[0], chlist[1])
