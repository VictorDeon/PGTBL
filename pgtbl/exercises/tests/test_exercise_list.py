from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ListExerciseTestCase(TestCase):
    """
    Test to list question into exercises.
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
        User can not see the exercises list without logged in.
        """

        pass

    def test_file_pagination(self):
        """
        Test to show question by pagination.
        """

        pass

    def test_users_can_see_the_exercise_list(self):
        """
        User like students, monitors and teacher can see the exercises list
        with exercises questions.
        """

        pass
