from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from model_mommy import mommy
from TBLSessions.models import TBLSession
from disciplines.models import Discipline
from questions.models import (
    Question, Alternative
)
from TBLSessions.models import TBLSession
from disciplines.models import Discipline

User = get_user_model()


class UpdateQuestionTestCase(TestCase):
    """
    Test to update a question to exercise and tests.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.question = mommy.make('Question')
        self.session = mommy.make('TBLSession')

        self.alternatives = mommy.make('Alternative', _quantity=4)
        self.alternatives[0].is_correct = True
        self.alternatives[0].save()

        self.session.questions.add(self.question)
        self.question.alternatives.set(self.alternatives)

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
            is_staff=True,
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

        self.url = reverse('questions:update-question',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk,
                                   'question_id': self.question.id})


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
        User can not update a question without logged in.
        """

        url = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        response = self.client.get(url,follow=True)
        self.assertRedirects(response, '/login/?next='+url, status_code=302,
            target_status_code=200,fetch_redirect_response=True)


    def test_update_question_by_teacher(self):
        """
        Test to update a question and alternatives by teacher.
        """

        url = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        self.client.login(username=self.teacher.username, password=self.teacher.password)


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

        response = self.client.get(url, follow=True)
        self.assertRedirects(response, '/login/?next='+url, status_code=302,
            target_status_code=200,fetch_redirect_response=True)

    def test_update_question_by_monitors(self):
        """
        Test to update a question and alternatives by monitors.
        """

        pass

    def test_update_question_fail(self):
        """
        User can not update a question with invalid fields and alternativas.
        """

        pass

    def test_create_question_by_student_fail(self):
        """
        Student can not update a question with alternatives.
        """

        pass

    def test_update_only_one_alternative_correct(self):
        """
        Teacher or Monitor can update only one alternative in the question
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
            'is_exercise': False,

            'alternatives-0-title': "A",
            'alternatives-0-is_correct': True,

            'alternatives-1-title': "B",
            'alternatives-1-is_correct': True,

            'alternatives-2-title': "C",
            'alternatives-2-is_correct': True,

            'alternatives-3-title': "D",
            'alternatives-3-is_correct': False,

        }

        response = self.client.post(self.url, data=data)
        alter = response.context_data['alternatives']

        self.assertIsNotNone(response.context_data['alternatives'][0]._errors)
        self.assertIsNotNone(response.context_data['alternatives'][1]._errors)
        self.assertIsNotNone(response.context_data['alternatives'][2]._errors)
        self.assertIsNotNone(response.context_data['alternatives'][3]._errors)
        self.assertEqual(Alternative.objects.all().count(), 4)

    def test_update_four_alternatives_in_a_question(self):
        """
        A question need to have four alternatives. Can not update a question
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
            'is_exercise': False,

            'alternatives-0-title': "A",
            'alternatives-0-is_correct': True,

            'alternatives-1-title': "B",
            'alternatives-1-is_correct': False,

            'alternatives-2-title': "C",
            'alternatives-2-is_correct': False,

            'alternatives-3-title': "",
            'alternatives-3-is_correct': None,
        }

        response = self.client.post(self.url, data=data)
        self.assertIsNotNone(response.context_data['alternatives'][0]._errors)
        self.assertIsNotNone(response.context_data['alternatives'][1]._errors)
        self.assertIsNotNone(response.context_data['alternatives'][2]._errors)
        self.assertIsNotNone(response.context_data['alternatives'][3]._errors)
        self.assertEqual(Alternative.objects.all().count(), 4)