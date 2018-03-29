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


class CreateQuestionTestCase(TestCase):
    """
    Test to create a new question to exercise and tests.
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
        User can not create a new question without logged in.
        """

        pass

    def test_create_question_by_teacher(self):
        """
        Test to create a new question with alternatives by teacher.
        """

        pass

    def test_create_question_by_monitors(self):
        """
        Test to create a new question and alternatives by monitors.
        """

        pass

    def test_create_question_fail(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        pass

    def test_create_question_by_student_fail(self):
        """
        Student can not create a question with alternatives.
        """

        pass

    def test_create_only_one_alternative_correct(self):
        """
        Teacher or Monitor can create only one alternative in the question
        with correct answer, can not be 4, 3, or 2 correct answer.
        """

        pass

    def test_create_four_alternatives_in_a_question(self):
        """
        A question need to have four alternatives. Can not create a question
        with 3 or 2 or 1 alternative.
        """

        pass
