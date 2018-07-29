from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class DeleteQuestionTestCase(TestCase):
    """
    Test to delete a question.
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
        User can not delete a question without logged in.
        """

        pass

    def test_delete_question_by_teacher(self):
        """
        Test to delete a question by teacher.
        """

        pass

    def test_delete_question_by_monitors(self):
        """
        Test to delete a question by monitors.
        """

        pass

    def test_delete_question_by_student_fail(self):
        """
        Student can not delete a question.
        """

        pass

    def test_delete_alternatives_when_delete_question(self):
        """
        Test to delete all alternatives when delete a specific question.
        """

        pass
