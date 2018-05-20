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

        self.url = reverse('questions:create-question',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk})


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

        print(url)
        response = self.client.get(url,follow=True)
        print(response.redirect_chain)
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
        print(response.redirect_chain)
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

        pass

    def test_update_four_alternatives_in_a_question(self):
        """
        A question need to have four alternatives. Can not update a question
        with 3 or 2 or 1 alternative.
        """

        pass
