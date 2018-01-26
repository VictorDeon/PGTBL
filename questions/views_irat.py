from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView, FormView
)

# CSV
from django.http import HttpResponse
import csv

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from .models import Question, Submission
from .forms import AnswerQuestionForm


class IRATView(LoginRequiredMixin,
               PermissionMixin,
               ListView):
    """
    iRAT (Individual Readiness Assurance Test)
    """

    template_name = 'questions/irat.html'
    paginate_by = 1
    context_object_name = 'questions'

    # Permissions
    permissions_required = []

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session and form into exercise list context data.
        """

        context = super(IRATView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['form1'] = AnswerQuestionForm(prefix="alternative01")
        context['form2'] = AnswerQuestionForm(prefix="alternative02")
        context['form3'] = AnswerQuestionForm(prefix="alternative03")
        context['form4'] = AnswerQuestionForm(prefix="alternative04")
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        session = self.get_session()

        questions = Question.objects.filter(
            session=session,
            is_exercise=False
        )

        return questions


class AnswerIRATQuestionView(FormView):
    """
    Answer the respective iRAT question.
    """

    template_name = 'questions/irat-list.html'
    form_class = AnswerQuestionForm

    # Permissions
    permissions_required = []

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Get question by url kwargs.
        """

        question = get_object_or_404(
            Question,
            pk=self.kwargs.get('question_id', '')
        )

        return question

    def get_page(self):
        """
        Get the page that the questions is inserted.
        """

        page = self.kwargs.get('question_page', '')

        return page

    def get_success_url(self):
        """
        After answer the question the same page.
        """

        success_url = reverse_lazy(
            'questions:irat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        success_url += "?page={0}".format(self.get_page())

        return success_url

    def post(self, request, *args, **kwargs):
        """
        Form to insert scores and answer question.
        """

        question = self.get_object()

        form1 = AnswerQuestionForm(request.POST, prefix="alternative01")
        form2 = AnswerQuestionForm(request.POST, prefix="alternative02")
        form3 = AnswerQuestionForm(request.POST, prefix="alternative03")
        form4 = AnswerQuestionForm(request.POST, prefix="alternative04")

        success = False

        if form1.is_valid() and \
           form2.is_valid() and \
           form3.is_valid() and \
           form4.is_valid():

            score = self.get_question_score(
                question=question,
                forms=[form1, form2, form3, form4]
            )

            scores = self.get_form_scores(
                forms=[form1, form2, form3, form4]
            )

            success = self.validate_answer(scores, question)

            correct_alternative = None
            for alternative in question.alternatives.all():
                if alternative.is_correct:
                    correct_alternative = alternative

            if success:
                messages.success(
                    self.request,
                    _("Question answered successfully.")
                )

                submission = Submission.objects.create(
                    user=self.request.user,
                    question=question,
                    correct_alternative=correct_alternative.title,
                    exam='iRAT',
                    score=score
                )

        return redirect(self.get_success_url())

    def get_question_score(self, question, forms):
        """
        Get the score from correct alternative.
        """

        form1, form2, form3, form4 = forms
        score = 0

        if question.alternatives.all()[0].is_correct:
            score = int(form1['score'].value())
        elif question.alternatives.all()[1].is_correct:
            score = int(form2['score'].value())
        elif question.alternatives.all()[2].is_correct:
            score = int(form3['score'].value())
        else:
            score = int(form4['score'].value())

        return score


    def get_form_scores(self, forms):
        """
        Get the total scores from forms.
        """

        scores = 0

        for form in forms:
            scores += int(form['score'].value())

        return scores


    def validate_answer(self, scores, question):
        """
        Validate the submission.
        """

        if 0 <= scores <= 4:

            submissions = Submission.objects.filter(
                question=question,
                user=self.request.user,
                exam='iRAT'
            )

            if submissions.count() == 0:
                return True

            messages.error(
                self.request,
                _("You can only submit the question once.")
            )

            return False

        messages.error(
            self.request,
            _("You only have 4 points to distribute to the \
              4 alternatives.")
        )

        return False


class IRATResultView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    Show the result of iRAT test.
    """

    template_name = 'questions/irat-result.html'
    context_object_name = 'submissions'

    # Permissions
    permissions_required = []

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_questions(self):
        """
        Get all exercise list questions.
        """

        questions = Question.objects.filter(
            session=self.get_session(),
            is_exercise=False
        )

        return questions

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session into exercise result context data.
        """

        context = super(IRATResultView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['result'] = self.result()
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        submissions = Submission.objects.filter(
            user=self.request.user,
            exam='iRAT'
        )

        return submissions

    def result(self):
        """
        Get the total scores about exercise list.
        """

        questions = self.get_questions()
        submissions = self.get_queryset()

        score = 0
        grade = 0

        total = 4*questions.count()

        for submission in submissions:
            score += submission.score

        if total > 0:
            grade = (score/total) * 10

        result = {
            'score': score,
            'total': total,
            'grade': "{0:.2f}".format(grade)
        }

        return result


def get_csv(request, *args, **kwargs):
    """
    Create a CSV about exercise list result.
    """

    # Create the HttpResponse object with the approprieate CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exercise-result.csv"'

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
        is_exercise=False
    )

    submissions = Submission.objects.filter(
        user=request.user,
        exam='iRAT'
    )

    score = 0
    total = 4*questions.count()

    for submission in submissions:
        score += submission.score

    grade = (score/total) * 10

    # Create CSV file rows
    writer.writerow([
        'ID: {0}'.format(request.user.id),
        'Nome: {0}'.format(request.user.get_short_name()),
        'Username: {0}'.format(request.user.username),
        'Tipo de avaliação: iRAT',
    ])
    writer.writerow([
        'Disciplina: {0}'.format(discipline.title),
        'Professor: {0}'.format(discipline.teacher),
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
