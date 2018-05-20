from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from model_mommy import mommy
from questions.models import (
    Question, Alternative
)
from TBLSessions.models import TBLSession
from disciplines.models import Discipline

User = get_user_model()


class CreateQuestionTestCase(TestCase):
    """
    Test to create a new question to exercise and tests.
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

        self.monitor = User.objects.create_user(
            username='monitor',
            email='monitor@gmail.com',
            password='test1234',
        )
        self.session.discipline.monitors.add(self.monitor)

        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@gmail.com',
            password='test1234',
            is_teacher=True,
        )
        self.session.discipline.teacher = self.teacher
        self.session.discipline.save()

        self.url = reverse('questions:create-question',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        Question.objects.all().delete()
        TBLSession.objects.all().delete()
        Discipline.objects.all().delete()
        Alternative.objects.all().delete()

    def test_redirect_to_login(self):
        """
        User can not create a new question without logged in.
        """
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_create_question_by_teacher(self):
        """
        Test to create a new question with alternatives by teacher.
        """

        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

        }

        self.client.post(self.url, data=data)
        self.assertEqual(Question.objects.all().count(), 1)

    def test_create_question_by_monitors(self):
        """
        Test to create a new question and alternatives by monitors.
        """

        self.client.login(username=self.monitor.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

        }

        self.client.post(self.url, data=data)
        self.assertEqual(Question.objects.all().count(), 1)

    def test_alternative_question_fail(self):
        """
        User can not create a question's alternatives with invalid fields.
        """

        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': False,

                'alternatives-0-title': 123,
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "",
                'alternatives-1-is_correct': True,

                'alternatives-2-title': "",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "",
                'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        self.assertIsNotNone(response.context_data['alternatives'][0].errors)
        self.assertIsNotNone(response.context_data['alternatives'][1].errors)
        self.assertIsNotNone(response.context_data['alternatives'][2].errors)
        self.assertIsNotNone(response.context_data['alternatives'][3].errors)
        self.assertEqual(Alternative.objects.all().count(), 0)

    def test_create_question_fail(self):
        """
        User can not create a question with invalid fields and alternatives.
        """

        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': 3,
                'topic': [],
                'level': '',
                'is_exercise': False,

                'alternatives-0-title': 123,
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "",
                'alternatives-1-is_correct': True,

                'alternatives-2-title': "",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "",
                'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        self.assertIsNotNone(response.context_data['form'].errors)
        self.assertEqual(Question.objects.all().count(), 0)

    def test_create_question_by_student_fail(self):
        """
        Student can not create a question with alternatives.
        """

        self.client.login(username=self.student.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(Alternative.objects.all().count(), 0)
        self.assertEqual(Question.objects.all().count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_teacher_create_only_one_alternative_correct(self):
        """
        Teacher can create only one alternative in the question
        with correct answer, can not be 4, 3, or 2 correct answer.
        """

        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(Question.objects.all().count(), 1)
        self.assertEqual(Alternative.objects.all().count(), 4)

    def test_monitor_create_only_one_alternative_correct(self):
        """
        Monitor can create only one alternative in the question
        with correct answer, can not be 4, 3, or 2 correct answer.
        """

        self.client.login(username=self.monitor.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(Question.objects.all().count(), 1)
        self.assertEqual(Alternative.objects.all().count(), 4)

    def test_create_question_with_more_than_one_alternative_correct(self):
        """
        Monitor or Teacher can create only one alternative in the question
        with correct answer, can not be 4, 3, or 2 correct answer.
        """

        self.client.login(username=self.monitor.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': True,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,
        }

        response = self.client.post(self.url, data=data)
        self.assertIsNotNone(response.context_data['form'].errors)
        self.assertEqual(Question.objects.all().count(), 0)
        self.assertEqual(Alternative.objects.all().count(), 0)

    def test_create_four_alternatives_in_a_question(self):
        """
        A question need to have four alternatives. Can not create a question
        with 3 or 2 or 1 alternative.
        """
        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(Question.objects.all().count(), 1)

    def test_create_one_alternative_in_a_question(self):
        """
        A question need to have four alternatives. Can not create a question
        with value < min bound
        """
        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,
        }

        response = self.client.post(self.url, data=data)
        self.assertIsNotNone(response.context_data['form'].errors)
        self.assertEqual(Alternative.objects.all().count(), 0)

    def test_create_5_alternatives_in_a_question(self):
        """
        A question need to have four alternatives. Can not create a question
        with value > max bound.
        """
        self.client.login(username=self.teacher.username, password='test1234')

        data = {
                'alternatives-TOTAL_FORMS': '4',
                'alternatives-INITIAL_FORMS': '0',
                'alternatives-MAX_NUM_FORMS': '4',

                'title': "Questao 01",
                'topic': "Testes de Software",
                'level': 'Basic',
                'is_exercise': True,

                'alternatives-0-title': "Alternativa 0",
                'alternatives-0-is_correct': True,

                'alternatives-1-title': "Alternativa 1",
                'alternatives-1-is_correct': False,

                'alternatives-2-title': "Alternativa 2",
                'alternatives-2-is_correct': False,

                'alternatives-3-title': "Alternativa 3",
                'alternatives-3-is_correct': False,

                'alternatives-4-title': "Alternativa 4",
                'alternatives-4-is_correct': False,
        }

        self.client.post(self.url, data=data)
        self.assertEqual(Alternative.objects.all().count(), 4)
