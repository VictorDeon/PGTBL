from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView

from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from groups.models import Group
from questions.models import Question, GRATSubmission
from questions.forms import AnswerGRATQuestionForm


class GRATAnswerQuestionView(LoginRequiredMixin, FormView):
    """
    Answer the respective gRAT question.
    """

    template_name = 'grat/grat.html'
    form_class = AnswerGRATQuestionForm

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
