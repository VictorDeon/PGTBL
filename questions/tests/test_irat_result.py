from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from core.roles import Teacher
from model_mommy import mommy
from questions.views_irat import (
    IRATResultView
)
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from django.utils import timezone
import pytz
from disciplines.models import Discipline
from TBLSessions.models import TBLSession

User = get_user_model()


class IRATResultTestCase(TestCase):
    """
    Test to show irat test result.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.teacher = User.objects.create()

        self.discipline = Discipline.objects.create(
                title = 'Test',
                teacher_id = self.teacher.id
        )

        self.session = TBLSession.objects.create(
                discipline_id = self.discipline.id,
        )

        self.question = Question.objects.create(
                session_id = self.session.id
        )

        self.irat = IRATResultView()

    def tearDown(self):
        """
        This method will run after any test.
        """
        TBLSession.objects.all().delete()
        Discipline.objects.all().delete()
        User.objects.all().delete()
        IRATSubmission.objects.all().delete()

    def test_user_can_see_irat_result(self):

        """
        User like student, teacher and monitors can see the result of irat
        after the test is over or if student finish the test.
        """

        pass

    def test_show_only_not_exercise_question(self):
        """
        Show only not exercise question that are into irat test, and show the
        answers.
        """

        pass

    def test_calcule_the_irat_result(self):

        """
        Calcule the irat test result from irat test.
        score that the user made, total of scores and grade of user.
        Only students have grade created.
        """

    #    response = self.client.post(
    #         reverse_lazy(
    #             'questions:irat-result',
    #             kwargs = {'slug': self.teacher.id, 'pk': self.irat.get_session() }),
    #             {'result': result}
    #        )
    #    assert(response)
        pass
