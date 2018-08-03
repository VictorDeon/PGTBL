from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession
from questions.models import Question, Alternative

User = get_user_model()


class CreateQuestionTestCase(TestCase):
    """
    Test to create a new question to exercises and tests.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.teacher_monitor = user_factory(name="otavio", is_teacher=True)
        self.student = user_factory(name="joao", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student],
            monitors=[self.monitor, self.teacher_monitor]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test"
        )
        self.data = {
            'title': "Question 01",
            'topic': "Topic 01",
            'level': 'Basic',
            'session': self.module,
            'alternatives-TOTAL_FORMS': '4',
            'alternatives-INITIAL_FORMS': '0',
            'alternatives-MIN_NUM_FORMS': '0',
            'alternatives-MAX_NUM_FORMS': '4',
            'alternatives-0-title': "Alternative 0",
            'alternatives-0-is_correct': True,
            'alternatives-1-title': "Alternative 1",
            'alternatives-1-is_correct': False,
            'alternatives-2-title': "Alternative 2",
            'alternatives-2-is_correct': False,
            'alternatives-3-title': "Alternative 3",
            'alternatives-3-is_correct': False,
        }
        self.url = reverse_lazy(
            'questions:create-question',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.module.delete()

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_create_question_by_student_fail(self):
        """
        Student can not create a question with alternatives.
        """

        self.client.login(username=self.student.username, password='test1234')
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        check_messages(
            self, response,
            tag="alert-danger",
            content="You are not authorized to do this action."
        )

    def test_create_question_by_user_fail(self):
        """
        User that is not into discipline can not create a question with alternatives.
        """

        self.client.login(username=self.user.username, password='test1234')
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        check_messages(
            self, response,
            tag="alert-danger",
            content="You are not authorized to do this action."
        )

    def test_create_question_by_teacher(self):
        """
        Test to create a new question with alternatives by teacher.
        """

        self.client.login(username=self.teacher.username, password='test1234')

        self.verify_create_question_ok()

    def test_create_question_by_monitors(self):
        """
        Test to create a new question and alternatives by monitors.
        """

        self.client.login(username=self.monitor.username, password='test1234')

        self.verify_create_question_ok()

    def test_create_question_fail_two_correct_answer(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-1-is_correct'] = True

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_three_correct_answer(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-1-is_correct'] = True
        self.data['alternatives-2-is_correct'] = True

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_four_correct_answer(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-1-is_correct'] = True
        self.data['alternatives-2-is_correct'] = True
        self.data['alternatives-3-is_correct'] = True

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_three_alternatives(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-0-title'] = ""

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_two_alternatives(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-0-title'] = ""
        self.data['alternatives-1-title'] = ""

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_one_alternative(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-0-title'] = ""
        self.data['alternatives-1-title'] = ""
        self.data['alternatives-2-title'] = ""

        self.verify_field_error_validation(self.data)

    def verify_create_question_ok(self):
        """
        Verify that the creation is correct
        """

        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        check_messages(
            self, response,
            tag="alert-success",
            content="Question created successfully."
        )

    def verify_field_error_validation(self, data):
        """
        Verify field error validation.
        """
        self.client.login(username=self.teacher.username, password='test1234')

        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)

        return response
