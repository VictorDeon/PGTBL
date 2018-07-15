from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)

User = get_user_model()


class IRATResultTestCase(TestCase):
    """
    Test to show irat test result.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        pass

    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

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

        pass
