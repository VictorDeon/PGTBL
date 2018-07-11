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


class ListExerciseTestCase(TestCase):
    """
    Test to list question into exercise.
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

    def test_redirect_to_login(self):
        """
        User can not see the exercise list without logged in.
        """

        pass

    def test_file_pagination(self):
        """
        Test to show question by pagination.
        """

        pass

    def test_users_can_see_the_exercise_list(self):
        """
        User like students, monitors and teacher can see the exercise list
        with exercise questions.
        """

        pass
