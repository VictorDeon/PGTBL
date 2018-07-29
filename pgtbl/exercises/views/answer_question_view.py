from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView

from disciplines.models import Discipline
from modules.models import TBLSession
from questions.models import Question
from exercises.models import ExerciseSubmission
from questions.forms import AnswerQuestionForm


class AnswerQuestionView(LoginRequiredMixin, FormView):
    """
    Answer the respective question.
    """

    template_name = 'exercises/list.html'
    form_class = AnswerQuestionForm

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
            'exercises:list',
            kwargs={
                'slug': discipline.slug,
                'pk': session.id
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

                ExerciseSubmission.objects.create(
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

            submissions = ExerciseSubmission.objects.filter(
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
