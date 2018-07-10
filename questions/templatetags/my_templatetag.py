from django import template

from questions.models import GRATSubmission
from groups.models import Group

register = template.Library()
@register.filter(name='filterGRAT')
def filterGRAT(question,user):

    discipline = question.session.discipline
    group = user.student_groups.all().filter(discipline=discipline)
    session = question.session

    try:
         submission = GRATSubmission.objects.get(session=session,group=group,question=question)
    except Exception as e:
        return False

    if  submission == None:
        return False

    return submission.score
