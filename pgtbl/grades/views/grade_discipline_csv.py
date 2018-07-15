from django.http import HttpResponse
import csv

from disciplines.models import Discipline
from grades.models import FinalGrade


def get_final_grade_csv(request, *args, **kwargs):
    """
    Create a CSV from students final grade.
    """

    # Create the HttpResponse object with the approprieate CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="final-grades.csv"'

    # Create the CSV writer
    writer = csv.writer(response)

    # Get important variables
    discipline = Discipline.objects.get(
        slug=kwargs.get('slug', '')
    )

    grades = FinalGrade.objects.filter(
        discipline=discipline
    )

    # Create CSV file rows
    writer.writerow([
        'Disciplina',
        'Usuários',
        'Nota final',
        'Status'
    ])

    for grade in grades:
        if grade.calcule_final_grade() > 5:
            status = 'Aprovado'
        else:
            status = 'Reprovado'

        writer.writerow([
            '{0}'.format(discipline.title),
            '{0}'.format(grade.student.username),
            '{0:.1f}'.format(grade.calcule_final_grade()),
            '{0}'.format(status)
        ])

    return response
