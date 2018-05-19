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

from TBLSessions.models import TBLSession
from disciplines.models import Discipline

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
        self.question = mommy.make('Question')
        self.session.questions.add(self.question)

        self.student = User.objects.create_user(
            username='student',
            email='teste@gmail.com',
            password='test1234',
        )
        self.session.discipline.students.add(self.student)

        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@gmail.com',
            password='test1234',
        )
        self.session.discipline.teacher = self.teacher
        self.session.discipline.save()

        self.monitor = User.objects.create_user(
            username='monitor',
            email='monitor@gmail.com',
            password='test1234',
        )
        self.session.discipline.monitors.add(self.monitor)

        self.student_not_associated = User.objects.create_user(
            username='student123',
            email='teste123@gmail.com',
            password='test1234',
        )

        self.url = reverse('questions:list',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk})

        self.url_submit_answer = reverse('questions:exercise-answer-question',
                                         kwargs={'slug': self.session.
                                                 discipline.slug,
                                                 'pk': self.session.pk,
                                                 'question_id': self.question.
                                                 id,
                                                 'question_page': 1})

    def tearDown(self):
        """
        This method will run after any test.
        """
        User.objects.all().delete()
        Question.objects.all().delete()
        TBLSession.objects.all().delete()
        Discipline.objects.all().delete()

        pass

    def test_user_student_can_answer(self):
        """
        User like student, monitor and teacher can answer a question and
        create a submission.
        """
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)

        self.assertIsNotNone(response.context['form1'])
        self.assertIsNotNone(response.context['form2'])
        self.assertIsNotNone(response.context['form3'])
        self.assertIsNotNone(response.context['form4'])

    def test_user_monitor_can_answer(self):
        """
        User like student, monitor and teacher can answer a question and
        create a submission.
        """
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)

        self.assertIsNotNone(response.context['form1'])
        self.assertIsNotNone(response.context['form2'])
        self.assertIsNotNone(response.context['form3'])
        self.assertIsNotNone(response.context['form4'])

    def test_user_teacher_can_answer(self):
        """
        User like student, monitor and teacher can answer a question and
        create a submission.
        """
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)

        self.assertIsNotNone(response.context['form1'])
        self.assertIsNotNone(response.context['form2'])
        self.assertIsNotNone(response.context['form3'])
        self.assertIsNotNone(response.context['form4'])

    def test_not_logged_user_cannot_answer(self):
        """
        User not logged in is redirected to the login page
        """
        response = self.client.get(self.url)

        response.context

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
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)

        data = {
            'alternative01-score': 1,
            'alternative02-score': 1,
            'alternative03-score': 1,
            'alternative04-score': 1,
        }

        response2 = self.client.post(self.url_submit_answer, data=data)
        import ipdb; ipdb.set_trace()

        print(response.status_code)

    def test_only_submit_one_time(self):
        """
        User can only submit a answer once.
        """

        pass
