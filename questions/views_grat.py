from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views.generic import (
    ListView, FormView, UpdateView, DetailView
)
from django import template

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes
from grades.models import Grade
from groups.models import Group
from .models import Question, GRATSubmission
from .forms import AnswerGRATQuestionForm, GRATDateForm, GRATForm

# Python imports
from datetime import timedelta


class GRATView(LoginRequiredMixin,
               PermissionMixin,
               ListView):
    """
    gRAT (Group Readiness Assurance Test)
    """

    template_name = 'questions/grat.html'
    paginate_by = 1
    context_object_name = 'questions'

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'grat_permissions'
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
            'TBLSessions:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
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
        Insert discipline, session and form into gRAT context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(GRATView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['date_form'] = GRATDateForm()
        context['grat_form'] = GRATForm()
        context['form1'] = AnswerGRATQuestionForm(prefix="alternative01")
        context['form2'] = AnswerGRATQuestionForm(prefix="alternative02")
        context['form3'] = AnswerGRATQuestionForm(prefix="alternative03")
        context['form4'] = AnswerGRATQuestionForm(prefix="alternative04")

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


class GRATUpdateView(LoginRequiredMixin,
                     PermissionMixin,
                     UpdateView):
    """
    Update the gRAT duration and weight
    """

    model = TBLSession
    template_name = 'questions/grat.html'
    form_class = GRATForm

    # Permissions
    permissions_required = ['crud_tests']

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        messages.success(self.request, _('gRAT updated successfully.'))

        return super(GRATUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'questions:grat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url


class GRATDateUpdateView(LoginRequiredMixin,
                         PermissionMixin,
                         UpdateView):
    """
    Update the gRAT date.
    """

    model = TBLSession
    template_name = 'questions/grat.html'
    form_class = GRATDateForm

    # Permissions
    permissions_required = ['crud_tests']

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """

        now = timezone.localtime(timezone.now())

        if form.instance.grat_datetime is None:

            messages.error(
                self.request,
                _("gRAT date must to be filled in.")
            )

            return redirect(self.get_success_url())

        if now > form.instance.grat_datetime:

            messages.error(
                self.request,
                _("gRAT date must to be later than today's date.")
            )

            return redirect(self.get_success_url())

        if (form.instance.irat_datetime + \
            timedelta(minutes=form.instance.irat_duration)) > \
            form.instance.grat_datetime:

            messages.error(
                self.request,
                _("gRAT date must to be later than iRAT date with its duration.")
            )

            return redirect(self.get_success_url())

        messages.success(self.request, _('gRAT date updated successfully.'))

        return super(GRATDateUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'questions:grat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url

class AnswerGRATQuestionView(FormView):
    """
    Answer the respective gRAT question.
    """

    template_name = 'questions/grat.html'
    form_class = AnswerGRATQuestionForm

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'grat_permissions'
    ]

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        submissions = self.get_GRAT_submission()

        return submissions

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'TBLSessions:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
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

    def get_student_group(self):
        """
        Get current student group.
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if self.request.user in group.students.all():
                return group

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
            'questions:grat-list',
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

        form1 = AnswerGRATQuestionForm(request.POST, prefix="alternative01")
        form2 = AnswerGRATQuestionForm(request.POST, prefix="alternative02")
        form3 = AnswerGRATQuestionForm(request.POST, prefix="alternative03")
        form4 = AnswerGRATQuestionForm(request.POST, prefix="alternative04")

        success = False

        if form1.is_valid() and \
           form2.is_valid() and \
           form3.is_valid() and \
           form4.is_valid():

            score = self.get_question_score(
                question=question,
                forms=[form1, form2, form3, form4]
            )

            success = self.validate_answer(
                question=question,
                forms=[form1, form2, form3, form4]
            )

            correct_alternative = None
            for alternative in question.alternatives.all():
                if alternative.is_correct:
                    correct_alternative = alternative

            if success:
                messages.success(
                    self.request,
                    _("Question answered successfully.")
                )

                GRATSubmission.objects.create(
                    session=self.get_session(),
                    group=self.get_student_group(),
                    user=self.request.user,
                    question=question,
                    correct_alternative=correct_alternative.title,
                    score=score
                )

        return redirect(self.get_success_url())

    def get_GRAT_submission(self):

        session = self.get_session()
        group = sef.get_student_group()
        question = self.get_object()

        grat_submissions = GRATSubmission.objects.get(session=session,group=group,question=question)

        return grat_submissions


    # def get_context_data(self, **kwargs):
    #
    #     context = super(AnswerGRATQuestionView, self).get_context_data(**kwargs)
    #     context['teste'] = self.get_object()
    #     return context
    # def get(self,request):
    #     context = super(GRATResultView, self).get_context_data(**kwargs)
    #     context['pagetitle'] = 'My special Title'
    #     return render(self.request,self.template_name,context)
    #
    # def get(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return self.render_to_response(context)
    #
    # def get_context_data(self, **kwargs):
    #     context = super(AnswerGRATQuestionView, self).get_context_data(**kwargs)
    #     context['plus_context_key'] = "plus_context"
    #     return context
    #
    # def get_form_kwargs(self):
    #     kwargs = super(AnswerGRATQuestionView, self).get_form_kwargs()
    #     kwargs['plus_context_key'] = "number"
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     context = FormView.get_context_data(self, **kwargs)
    #     context['teste'] = 'teste'
    #
    #     return context



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


    def validate_answer(self, question, forms):
        """
        Validate the submission.
        """

        # Verify is student is in some group
        if not self.get_student_group():
            messages.error(
                self.request,
                _("Student must be in a group to answer the test.")
            )

            return False

        # Verify repeated options
        answers = [0, 1, 2, 4]

        for form in forms:
            if int(form['score'].value()) in answers:
                answers.remove(int(form['score'].value()))

        if len(answers) != 0:

            messages.error(
                self.request,
                _("You can't repeat the options.")
            )

            return False

        # Verify if has only one submission from the user group
        submissions = GRATSubmission.objects.filter(
            session=self.get_session(),
            question=question,
            group=self.get_student_group()
        )

        if submissions.count() != 0:

            messages.error(
                self.request,
                _("Your group has already answered this question.")
            )

            return False

        return True


class GRATResultView(LoginRequiredMixin,
                     PermissionMixin,
                     ListView):
    """
    Show the result of gRAT test.
    """

    template_name = 'questions/grat_result.html'
    context_object_name = 'submissions'

    # Permissions
    permissions_required = [
        'show_questions_permission'
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

    def get_questions(self):
        """
        Get all exercise list questions.
        """

        questions = Question.objects.filter(
            session=self.get_session(),
            is_exercise=False
        )

        return questions

    def get_student_group(self):
        """
        Get current student group.
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if self.request.user in group.students.all():
                return group

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session into gRAT result context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(GRATResultView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['result'] = self.result()
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """

        submissions = GRATSubmission.objects.filter(
            session=self.get_session(),
            group=self.get_student_group()
        )

        return submissions

    def result(self):
        """
        Get the total scores about gRAT test and distribute for all students
        from group.
        """

        questions = self.get_questions()
        submissions = self.get_queryset()

        # Calcule the grade
        score = 0
        grade = 0

        total = 4*questions.count()

        for submission in submissions:
            score += submission.score

        if total > 0:
            grade = (score/total) * 10

        grades = Grade.objects.filter(
            session=self.get_session(),
            group=self.get_student_group()
        )

        for student_grade in grades:
            student_grade.grat = grade
            student_grade.save()

        # Store the result and return it
        result = {
            'score': score,
            'total': total,
            'grade': "{0:.2f}".format(grade)
        }

        return result
