from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views.generic import (
    ListView, FormView, UpdateView
)

# App imports
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes
from grades.models import Grade
from groups.models import Group
from .models import Question, IRATSubmission
from .forms import AnswerQuestionForm, IRATDateForm, IRATForm


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
    permissions_required = [
        'show_questions_permission',
        'irat_permissions'
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
        Insert discipline, session and form into exercise list context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(IRATView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['date_form'] = IRATDateForm()
        context['irat_form'] = IRATForm()
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


class IRATUpdateView(LoginRequiredMixin,
                     PermissionMixin,
                     UpdateView):
    """
    Update the iRAT duration and weight
    """

    model = TBLSession
    template_name = 'questions/irat.html'
    form_class = IRATForm

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

        messages.success(self.request, _('iRAT updated successfully.'))

        return super(IRATUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'questions:irat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url


class IRATDateUpdateView(LoginRequiredMixin,
                         PermissionMixin,
                         UpdateView):
    """
    Update the iRAT date.
    """

    model = TBLSession
    template_name = 'questions/irat.html'
    form_class = IRATDateForm

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

        if form.instance.irat_datetime is None:

            messages.error(
                self.request,
                _("iRAT date must to be filled in.")
            )

            return redirect(self.get_success_url())

        if now > form.instance.irat_datetime:

            messages.error(
                self.request,
                _("iRAT date must to be later than today's date.")
            )

            return redirect(self.get_success_url())

        messages.success(self.request, _('iRAT date updated successfully.'))

        return super(IRATDateUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy(
            'questions:irat-list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url

class AnswerIRATQuestionView(FormView):
    """
    Answer the respective iRAT question.
    """

    template_name = 'questions/irat-list.html'
    form_class = AnswerQuestionForm

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'irat_permissions'
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

                IRATSubmission.objects.create(
                    session=self.get_session(),
                    user=self.request.user,
                    question=question,
                    correct_alternative=correct_alternative.title,
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

            submissions = IRATSubmission.objects.filter(
                session=self.get_session(),
                question=question,
                user=self.request.user
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

    template_name = 'questions/irat_result.html'
    context_object_name = 'submissions'

    # Permissions
    permissions_required = [
        'show_questions_permission',
        'show_test_result'
    ]

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("The results only be available when gRAT is done.")
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

    def get_session(self, **kwargs):
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
        Insert discipline, session into iRAT result context data.
        """

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(IRATResultView, self).get_context_data(**kwargs)
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

        submissions = IRATSubmission.objects.filter(
            session=self.get_session(),
            user=self.request.user
        )

        return submissions

    def result(self):
        """
        Get the total scores about iRAT.
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

        # Create a grade for specific student
        discipline = self.get_discipline()

        grades = Grade.objects.filter(
            session=self.get_session(),
            student=self.request.user
        )

        if grades.count() == 0 and self.request.user in discipline.students.all():
            Grade.objects.create(
                session=self.get_session(),
                student=self.request.user,
                group=self.get_student_group(),
                irat=grade
            )

        # Store the result and return it
        result = {
            'score': score,
            'total': total,
            'grade': "{0:.2f}".format(grade)
        }

        return result
