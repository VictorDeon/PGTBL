from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import resolve, reverse
from core.test_utils import check_messages
from questions import views_question
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)

User = get_user_model()


class UpdateQuestionTestCase(TestCase):
    """
    Test to update a question to exercise and tests.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.question = mommy.make('Question')
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
                                   'question_id':self.question.id})


    def tearDown(self):
        """
        This method will run after any test.
        """
        self.question.delete()
        self.monitor.delete()
        self.teacher.delete()


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

        url_question = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        self.client.login(username=self.teacher.username, password='test1234')


        data = {
                'title': 'Questao 01',
                'topic': 'Testes de Software',
                'level': 'Basic',
                'is_exercise': True,
        }

        response = self.client.put(url_question, data=data)
        #print(response.redirect_chain)
        self.assertEqual(self.question.title, "Questao 01")

    def test_update_question_by_monitors(self):
        """
        Test to update a question and alternatives by monitors.
        """
        url_question = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        self.client.login(username=self.monitor.username, password='test1234')


        data = {
                'title': 'Questao 01',
                'topic': 'Testes de Software',
                'level': 'Basic',
                'is_exercise': True,
        }

        response = self.client.put(url_question, data=data)
        #print(response.redirect_chain)
        self.assertEqual(self.question.title, "Questao 01")

        pass

    def test_update_question_fail(self):
        """
        User can not update a question with invalid fields and alternativas.
        """
        url_question = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        self.client.login(username=self.monitor.username, password='test1234')

        data = {
            'title': 'Questao 01',
            'topic': '',
            'level': 'Basic',
            'is_exercise': True,
        }

        response = self.client.put(url_question, data=data)

        self.assertNotEqual(self.question.title, "Questao 01")

    def test_create_question_by_student_fail(self):
        """
        Student can not update a question with alternatives.
        """

        url_question = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        self.client.login(username=self.student.username, password='test1234')

        data = {
            'title': 'Questao 01',
            'topic': 'Testes de Software',
            'level': 'Basic',
            'is_exercise': True,
            'alternatives-0-title': 'Alternativa 1',
            'alternatives-0-is_correct': False,
            'alternatives-1-title': 'Alternativa 2',
            'alternatives-1-is_correct': False,
            'alternatives-2-title': 'Alternativa 2',
            'alternatives-2-is_correct': False,
            'alternatives-3-title': 'Alternativa 2',
            'alternatives-3-is_correct': True,
        }

        response = self.client.put(url_question, data=data)

        self.assertNotEqual(self.question.title, "Questao 01")

    def test_update_only_one_alternative_correct(self):
        """
        Teacher or Monitor can update only one alternative in the question
        with correct answer, can not be 4, 3, or 2 correct answer.
        """
        url_question = '/profile/{}/sessions/{}/questions/{}/edit/'.format(
            self.question.session.discipline.slug,
            self.question.session.discipline.pk,
            self.question.id
        )

        self.client.login(username=self.teacher.username, password='test1234')

        data = {
            'title': 'Questao 01',
            'topic': 'Testes de Software',
            'level': 'Basic',
            'is_exercise': True,
            'alternatives-0-title': 'Alternativa 1',
            'alternatives-0-is_correct': True,
            'alternatives-1-title': 'Alternativa 2',
            'alternatives-1-is_correct': True,
            'alternatives-2-title': 'Alternativa 3',
            'alternatives-2-is_correct': False,
            'alternatives-3-title': 'Alternativa 4',
            'alternatives-3-is_correct': True,
        }

        response = self.client.put(url_question, data=data)

        self.assertNotEqual(self.question.title, "Questao 01")



    def test_update_four_alternatives_in_a_question(self):
        """
        A question need to have four alternatives. Can not update a question
        with 3 or 2 or 1 alternative.
        """

        pass
