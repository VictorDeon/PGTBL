from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.views.generic import CreateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.utils import get_datetimes
from questions.models import Question
from questions.forms import AlternativeFormSet


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
        'crud_question_permission'
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

        irat_datetime, grat_datetime = get_datetimes(self.get_session())

        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime
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

            if alternative_form.instance.title == '':

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
