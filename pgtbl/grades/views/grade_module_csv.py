from django.http import HttpResponse
import csv

from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from grades.models import Grade


def get_module_grade_csv(request, *args, **kwargs):
    """
    Create a CSV from TBL module grades.
    """

    # Create the HttpResponse object with the approprieate CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="session-grades.csv"'

    # Create the CSV writer
    writer = csv.writer(response)

    # Get important variables
    discipline = Discipline.objects.get(
        slug=kwargs.get('slug', '')
    )

    session = TBLSession.objects.get(
        pk=kwargs.get('pk', '')
    )

    grades = Grade.objects.filter(
        session=session
    )

    # Create CSV file rows
    writer.writerow([
        'Disciplina'
        'Grupos',
        'Usuários',
        'iRAT',
        'gRAT',
        'Test prático',
        'Peer Review',
        'Nota final'
    ])

    for grade in grades:
        writer.writerow([
            '{0}'.format(discipline.title),
            '{0}'.format(grade.group.title),
            '{0}'.format(grade.student.username),
            '{0}'.format(grade.irat),
            '{0}'.format(grade.grat),
            '{0}'.format(grade.practical),
            '{0}'.format(grade.peer_review),
            '{0:.1f}'.format(grade.calcule_session_grade())
        ])

    return response
