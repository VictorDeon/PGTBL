from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, FormView, RedirectView
)

# CSV
from django.http import HttpResponse
import csv


# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from .models import Question
from .forms import AlternativeFormSet, AnswerQuestionForm


class ExerciseListView(LoginRequiredMixin,
                       PermissionMixin,
                       ListView):
    """
    View to see all the questions that the students will answer.
    """

    template_name = 'questions/list.html'
    paginate_by = 1
    context_object_name = 'questions'

    # Permissions
    permissions_required = [
        'show_exercise_permission'
    ]

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

        context = super(ExerciseListView, self).get_context_data(**kwargs)
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
            is_exercise=True
        )

        return questions


class CreateQuestionView(LoginRequiredMixin,
                         PermissionMixin,
                         CreateView):
    """
    View to create a new question with alternatives.
    """

    model = Question
    fields = ['title', 'level', 'topic', 'is_exercise']
    template_name = 'questions/add.html'

    permissions_required = [
        'crud_exercise_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the question belongs to.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the TBL session that the question belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and session and alternatives formset into add
        question template.
        """

        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        if self.request.POST:
            context['alternatives'] = AlternativeFormSet(self.request.POST)
        else:
            context['alternatives'] = AlternativeFormSet()

        return context

    def form_valid(self, form):
        """
        Receive the form already validated to create a new question with
        for alternatives to fill.
        """

        form.instance.session = self.get_session()

        context = self.get_context_data()
        alternatives = context['alternatives']

        # Before a view is called, django initializes a transaction. If the
        # response return with success, django commits the transaction. If
        # there are any exceptions, django roll back the database.
        # Atomic allows us to create a block of code within atomicity in the
        # database is guaranteed. If the code block runs successfully, the
        # modification are inserted into the database, if give an exception
        # the modifications are discarted
        with transaction.atomic():
            self.object = form.save(commit=False)

            if alternatives.is_valid():
                alternatives.instance = self.object

                success = self.validate_alternatives(alternatives)

                if not success:
                    return super(CreateQuestionView, self).form_invalid(form)

                form.save()
                alternatives.save()
            else:
                return self.form_invalid(form)

        messages.success(self.request, _('Question created successfully.'))

        return super(CreateQuestionView, self).form_valid(form)

    def validate_alternatives(self, alternatives):
        """
        Verify if only one alternative is correct and if it has 4 alternatives.
        """

        counter_true = 0
        counter_false = 0

        for alternative_form in alternatives:

            if alternative_form.instance.alternative_title == '':

                messages.error(
                    self.request,
                    _('All the alternatives need to be filled.')
                )

                return False

            if alternative_form.instance.is_correct is True:
                counter_true += 1
            else:
                counter_false += 1

            if counter_true > 1 or counter_false == 4:

                messages.error(
                    self.request,
                    _('The question only needs one correct alternative, \
                      check if there is more than one or no longer insert one')
                )

                return False

        return True

    def form_invalid(self, form):
        """
        Redirect to form with form errors.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the questions fields and \
              alternative fields correctly.")
        )

        return super(CreateQuestionView, self).form_invalid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url


class UpdateQuestionView(LoginRequiredMixin,
                         PermissionMixin,
                         UpdateView):
    """
    View to update a new question with alternatives.
    """

    model = Question
    fields = ['title', 'level', 'topic', 'is_exercise']
    template_name = 'questions/update.html'

    permissions_required = [
        'crud_exercise_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the question belongs to.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the TBL session that the question belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Take the specific question to update.
        """

        question = Question.objects.get(
            session=self.get_session(),
            pk=self.kwargs.get('question_id', '')
        )

        return question

    def get_context_data(self, **kwargs):
        """
        Insert discipline and session and alternatives formset into add
        question template.
        """

        context = super(UpdateQuestionView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()

        if self.request.POST:
            context['alternatives'] = AlternativeFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['alternatives'] = AlternativeFormSet(
                instance=self.object
            )

        return context

    def form_valid(self, form):
        """
        Receive the form already validated to update the question with
        for alternatives.
        """

        form.instance.session = self.get_session()

        context = self.get_context_data()
        alternatives = context['alternatives']

        with transaction.atomic():
            self.object = form.save(commit=False)

            if alternatives.is_valid():
                alternatives.instance = self.object

                success = self.validate_alternatives(alternatives)

                if not success:
                    return super(UpdateQuestionView, self).form_invalid(form)

                form.save()
                alternatives.save()
            else:
                return self.form_invalid(form)

        messages.success(self.request, _('Question updated successfully.'))

        return super(UpdateQuestionView, self).form_valid(form)

    def validate_alternatives(self, alternatives):
        """
        Verify if only one alternative is correct and if it has 4 alternatives.
        """

        counter_true = 0
        counter_false = 0

        for alternative_form in alternatives:

            if alternative_form.instance.alternative_title == '':

                messages.error(
                    self.request,
                    _('All the alternatives need to be filled.')
                )

                return False

            if alternative_form.instance.is_correct is True:
                counter_true += 1
            else:
                counter_false += 1

            if counter_true > 1 or counter_false == 4:

                messages.error(
                    self.request,
                    _('The question only needs one correct alternative, \
                      check if there is more than one or no longer insert one')
                )

                return False

        return True

    def form_invalid(self, form):
        """
        Redirect to form with form errors.
        """

        messages.error(
            self.request,
            _("Invalid fields, please fill in the questions fields and \
              alternative fields correctly.")
        )

        return super(UpdateQuestionView, self).form_invalid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        return success_url


class DeleteQuestionView(LoginRequiredMixin,
                         PermissionMixin,
                         DeleteView):
    """
    View to delete a specific question.
    """

    model = Question

    permissions_required = [
        'crud_exercise_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the TBL session that the question belongs to
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_object(self):
        """
        Take the specific question to delete.
        """

        question = Question.objects.get(
            session=self.get_session(),
            pk=self.kwargs.get('question_id', '')
        )

        return question

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        messages.success(self.request, _("Question deleted successfully."))

        return success_url


class AnswerQuestionView(FormView):
    """
    Answer the respective question.
    """

    template_name = 'questions/list.html'
    form_class = AnswerQuestionForm

    # Permissions
    permissions_required = [
        'show_exercise_permission'
    ]

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
        After answer the question go to next page.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
            }
        )

        success_url += "?page={0}#question".format(self.get_page())

        return success_url

    def post(self, request, *args, **kwargs):
        """
        Form to insert scores and answer question.
        """

        # alternatives form
        form1 = AnswerQuestionForm(request.POST, prefix="alternative01")
        form2 = AnswerQuestionForm(request.POST, prefix="alternative02")
        form3 = AnswerQuestionForm(request.POST, prefix="alternative03")
        form4 = AnswerQuestionForm(request.POST, prefix="alternative04")

        question = self.get_object()

        # question alternatives
        alternatives = []
        alternative01 = question.alternatives.all()[0]
        alternative02 = question.alternatives.all()[1]
        alternative03 = question.alternatives.all()[2]
        alternative04 = question.alternatives.all()[3]
        alternatives.append(alternative01)
        alternatives.append(alternative02)
        alternatives.append(alternative03)
        alternatives.append(alternative04)

        if form1.is_valid() and \
           form2.is_valid() and \
           form3.is_valid() and \
           form4.is_valid():

            alternative01.score = form1.instance.score
            alternative02.score = form2.instance.score
            alternative03.score = form3.instance.score
            alternative04.score = form4.instance.score

            success = self.validate_answer(question, alternatives)

        if success:
            messages.success(
                self.request,
                _("Question answered successfully.")
            )
        else:
            messages.error(
                self.request,
                _("You only have 4 points to distribute to the \
                  4 alternatives.")
            )

        return redirect(self.get_success_url())

    def validate_answer(self, question, alternatives):
        """
        Checks if the distribution of the points is fair and inserts
        the punctuation.
        """

        total_score = 0

        for alternative in alternatives:
            total_score += alternative.score

            if total_score > 4:
                return False

            alternative.save()

            if alternative.is_correct:
                question.score = alternative.score

        if not question.show_answer:
            question.show_answer = True

        question.save()

        return True


class ExerciseResultView(LoginRequiredMixin,
                         PermissionMixin,
                         ListView):
    """
    Show the result of exercise list.
    """

    template_name = 'questions/result.html'
    context_object_name = 'questions'

    # Permissions
    permissions_required = [
        'show_exercise_permission',
        'show_result_permission'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        failure_redirect_path = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        messages.error(
            self.request,
            _("Answer all question before you see the results.")
        )

        return failure_redirect_path

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
        Insert discipline, session into exercise result context data.
        """

        context = super(ExerciseResultView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['result'] = self.result()
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        session = self.get_session()

        questions = Question.objects.filter(
            session=session,
            is_exercise=True
        )

        return questions

    def result(self):
        """
        Get the total scores about exercise list.
        """

        questions = self.get_queryset()

        score = 0
        grade = 0

        total = 4*questions.count()

        for question in questions:
            score += question.score

        grade = (score/total) * 10

        result = {
            'score': score,
            'total': total,
            'grade': grade
        }

        return result


class ResetExerciseView(LoginRequiredMixin,
                        PermissionMixin,
                        RedirectView):
    """
    Reset the exercise.
    """

    permissions_required = [
        'show_exercise_permission',
        'show_result_permission'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        failure_redirect_path = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        messages.error(
            self.request,
            _("Answer all question before you see the results.")
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Get discipline by url slug
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

    def get_queryset(self):
        """
        Get a question by url slug
        """

        session = self.get_session()

        questions = Question.objects.filter(
            session=session,
            is_exercise=True
        )

        return questions

    def get_success_url(self):
        """
        Get the success url to redirect to.
        """

        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.pk
            }
        )

        return success_url

    def get(self, request, *args, **kwargs):
        """
        Reset exercise list.
        """

        questions = self.get_queryset()

        for question in questions:
            question.score = 0

            for alternative in question.alternatives.all():
                alternative.score = 0
                alternative.save()

            question.show_answer = False

            question.save()

        messages.success(
            self.request,
            _("Exercise list reseted successfully.")
        )

        return redirect(self.get_success_url())


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
        is_exercise=True
    )

    score = 0
    total = 4*questions.count()

    for question in questions:
        score += question.score

    grade = (score/total) * 10

    # Create CSV file rows
    writer.writerow([
        'ID: {0}'.format(request.user.id),
        'Nome: {0}'.format(request.user.get_short_name()),
        'Disciplina: {0}'.format(discipline.title),
        'Professor: {0}'.format(discipline.teacher),
        'Sessão do TBL: {0}'.format(session.title),
        'Nota no exercicio: {0}'.format(grade)
    ])

    counter = 0
    for question in questions:
        counter += 1
        writer.writerow([
            '[{0}]'.format(counter),
            'Título: {0}'.format(question.title),
            'Pontuação: {0}/{1}'.format(question.score, 4)
        ])

    writer.writerow([
        '',
        '',
        'Pontuação total: {0}/{1}'.format(score, total)
    ])

    return response
