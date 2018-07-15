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


class AnswerQuestionTestCase(TestCase):
    """
    Test to answer a question.
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

    def test_user_can_answer(self):
        """
        User like student, monitor and teacher can answer a question and
        create a submission.
        """

        pass

    def test_result_answer_validation(self):
        """
        The result need to be between 0 and 4 points.
        """

        pass

    def test_only_submit_one_time(self):
        """
        User can only submit a answer once.
        """

        pass
