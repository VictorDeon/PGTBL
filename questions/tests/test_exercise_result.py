from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)

User = get_user_model()


class ExerciseResultTestCase(TestCase):
    """
    Test to show exercise result.
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

    def test_user_can_see_exercise_result(self):
        """
        User like student, teacher and monitors can see the result of exercise.
        """

        pass

    def test_show_only_exercise_question(self):
        """
        Show only exercise question that are into exercise list with his
        result.
        """

        pass

    def test_calcule_the_exercise_result(self):
        """
        Calcule the exercise result from exercise list.
        score that the user made, total of scores and grade of user.
        """

        pass

    def test_reset_exercise_list(self):
        """
        Remove all submissions from exercise list.
        """

        pass
