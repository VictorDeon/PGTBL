from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ExerciseResultTestCase(TestCase):
    """
    Test to show exercises result.
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
        User like student, teacher and monitors can see the result of exercises.
        """

        pass

    def test_show_only_exercise_question(self):
        """
        Show only exercises question that are into exercises list with his
        result.
        """

        pass

    def test_calcule_the_exercise_result(self):
        """
        Calcule the exercises result from exercises list.
        score that the user made, total of scores and grade of user.
        """

        pass

    def test_reset_exercise_list(self):
        """
        Remove all submissions from exercises list.
        """

        pass
