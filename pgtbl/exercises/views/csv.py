from django.http import HttpResponse
import csv

from disciplines.models import Discipline
from modules.models import TBLSession
from questions.models import Question
from exercises.models import ExerciseSubmission


def get_csv(request, *args, **kwargs):
    """
    Create a CSV about exercises list result.
    """

    # Create the HttpResponse object with the approprieate CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exercises-result.csv"'

    # Create the CSV writer
    writer = csv.writer(response)

    # Get important variables
    discipline = Discipline.objects.get(
        slug=kwargs.get('slug', '')
    )

    session = TBLSession.objects.get(
        pk=kwargs.get('pk', '')
    )

    questions = Question.objects.filter(
        session=session,
        is_exercise=True
    )

    submissions = ExerciseSubmission.objects.filter(
        session=session,
        user=request.user
    )

    score = 0
    total = 4 * questions.count()

    for submission in submissions:
        score += submission.score

    grade = (score / total) * 10

    # Create CSV file rows
    writer.writerow([
        'ID: {0}'.format(request.user.id),
        'Nome: {0}'.format(request.user.get_short_name()),
        'Username: {0}'.format(request.user.username),
        'Tipo de avaliação: Exercícios',
    ])
    writer.writerow([
        'Disciplina: {0}'.format(discipline.title),
        '[professor](#l8-teacher): {0}'.format(discipline.teacher),
        'Sessão do TBL: {0}'.format(session.title),
        'Nota no exercicio: {0:.2f}'.format(grade)
    ])

    counter = 0
    for submission in submissions:
        counter += 1
        writer.writerow([
            '[{0}]'.format(counter),
            'Título: {0}'.format(submission.question.title),
            'Pontuação: {0}/{1}'.format(submission.score, 4)
        ])

    writer.writerow([
        '',
        '',
        'Pontuação total: {0}/{1}'.format(score, total)
    ])

    return response
