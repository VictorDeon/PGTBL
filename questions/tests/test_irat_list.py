from django.core.urlresolvers import reverse_lazy
from core.roles import Teacher
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from questions.views_irat import (
    IRATDateUpdateView
)


User = get_user_model()


class ListIRATTestCase(TestCase):
    """
    Test to list question into IRAT test.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.teacher = User.objects.create()

        self.discipline = Discipline.objects.create(
                title = 'Software Test',
                teacher_id = self.teacher.id
        )

        self.session = TBLSession.objects.create(
                discipline_id = self.discipline.id
        )

        self.question = Question.objects.create(
                session_id = self.session.id
        )

        self.irat = IRATSubmission.objects.create(
                user_id = self.teacher.id,
                session_id = self.session.id,
                question_id = self.question.id
        )


    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not see the irat test without logged in.
        """

        pass

    def test_irat_test_pagination(self):
        """
        Test to show question by pagination.
        """

        pass

    def test_users_can_see_the_irat_list(self):
        """
        User like students, monitors and teacher can see the irat test
        with not exercise questions and when the date of irat arrive.
        """

        pass

    def test_users_can_not_see_the_irat_test(self):
        """
        User like students and monitors can not see the irat test if the
        time is behind date/time of irat teste or time is after date/time
        of irat test with its duration.
        """

        pass

    def test_only_teacher_can_change_weight_and_time(self):
        """
        Only teacher can change the irat test weight and duration.
        """

        pass

    def test_only_teacher_can_change_date_and_time(self):
        """
        Only teacher can change date and time from irat test.
        """

        pass

    def test_date_and_time_not_can_be_blank(self):
        """
        The date and time of irat test not can be blank.
        """

        pass

    def test_date_and_time_need_to_be_bigger_than_today(self):
        """
        The date and time from irat test need to be bigger than the
        date and time from today.
        """
        pass
