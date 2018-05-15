from django.shortcuts import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)

from TBLSessions.models import TBLSessions
from Discipline.models import Discipline

User = get_user_model()


class AnswerQuestionTestCase(TestCase):
    """
    Test to answer a question.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.session = mommy.make('TBLSession')

        self.student = User.objects.create_user(
            username='student',
            email='teste@gmail.com',
            password='test1234',
        )
        self.session.discipline.students.add(self.student)

        self.student_not_associated = User.objects.create_user(
            username='student123',
            email='teste123@gmail.com',
            password='test1234',
        )

        self.url = reverse('questions:list',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """
        User.objects.all().delete()
        TBLSessions.objects.all().delete()
        Discipline.objects.all().delete()

        pass

    def test_user_can_answer(self):
        """
        User like student, monitor and teacher can answer a question and
        create a submission.
        """

        pass

    def test_not_logged_user_cannot_answer(self):
        """
        User not logged in is redirected to the login page
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_student_associated_can_answer(self):
        """
        Student logged in and associated with that discipline
        can answer the questions
        """
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_student_not_associated_cannot_answer(self):
        """
        Student logged in and nor associated with that discipline
        can not answer the questions
        """

        self.client.login(username=self.student_not_associated.username,
                          password='test1234')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

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
