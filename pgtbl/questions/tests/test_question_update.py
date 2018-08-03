from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession
from questions.models import Question, Alternative

User = get_user_model()


class UpdateQuestionTestCase(TestCase):
    """
    Test to update a question to exercises and tests.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
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
            monitors=[self.monitor]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test"
        )
        self.question = mommy.make(
            Question,
            title="Question",
            topic="Topic",
            level='Basic',
            is_exercise=True,
            session=self.module
        )
        self.alternatives = mommy.make(
            Alternative,
            title="Alternative",
            question=self.question,
            _quantity=4
        )
        self.alternatives[0].is_correct = True
        self.alternatives[0].save()
        self.data = {
            'title': "Question Updated",
            'topic': "Topic Updated",
            'level': 'Basic',
            'is_exercise': True,
            'session': self.module,
            'alternatives-TOTAL_FORMS': '4',
            'alternatives-INITIAL_FORMS': '4',
            'alternatives-MIN_NUM_FORMS': '0',
            'alternatives-MAX_NUM_FORMS': '4',
            'alternatives-0-title': "Alternative Updated",
            'alternatives-0-is_correct': False,
            'alternatives-0-id': self.alternatives[0].pk,
            'alternatives-0-question': self.question.pk,
            'alternatives-1-title': "Alternative",
            'alternatives-1-is_correct': False,
            'alternatives-1-id': self.alternatives[1].pk,
            'alternatives-1-question': self.question.pk,
            'alternatives-2-title': "Alternative Updated",
            'alternatives-2-is_correct': True,
            'alternatives-2-id': self.alternatives[2].pk,
            'alternatives-2-question': self.question.pk,
            'alternatives-3-title': "Alternative",
            'alternatives-3-is_correct': False,
            'alternatives-3-id': self.alternatives[3].pk,
            'alternatives-3-question': self.question.pk
        }
        self.redirect_url = reverse_lazy(
            'exercises:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'questions:update-question',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk,
                'question_id': self.question.pk
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.module.delete()
        Question.objects.all().delete()
        Alternative.objects.all().delete()

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_update_question_by_teacher(self):
        """
        Test to update a question and alternatives by teacher.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        self.verify_create_question_ok()

    def test_update_question_by_monitors(self):
        """
        Test to update a question and alternatives by monitors.
        """

        self.client.login(username=self.monitor.username, password='test1234')
        self.verify_create_question_ok()

    def test_create_question_by_student_fail(self):
        """
        Student can not update a question with alternatives.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, self.data, follow=True)
        self.question.refresh_from_db()
        for alternative in self.alternatives:
            alternative.refresh_from_db()
        self.assertEqual(self.question.title, "Question")
        self.assertEqual(self.alternatives[0].title, "Alternative")
        self.assertEqual(self.alternatives[0].is_correct, True)
        self.assertEqual(self.alternatives[2].title, "Alternative")
        self.assertEqual(self.alternatives[2].is_correct, False)
        check_messages(
            self, response,
            tag='alert-danger',
            content='You are not authorized to do this action.'
        )

    def test_create_question_by_user_fail(self):
        """
        User that is not into discipline can not update a question with alternatives.
        """

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.post(self.url, self.data, follow=True)
        self.question.refresh_from_db()
        for alternative in self.alternatives:
            alternative.refresh_from_db()
        self.assertEqual(self.question.title, "Question")
        self.assertEqual(self.alternatives[0].title, "Alternative")
        self.assertEqual(self.alternatives[0].is_correct, True)
        self.assertEqual(self.alternatives[2].title, "Alternative")
        self.assertEqual(self.alternatives[2].is_correct, False)
        check_messages(
            self, response,
            tag='alert-danger',
            content='You are not authorized to do this action.'
        )

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

    def test_create_question_fail_one_alternatives(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-0-title'] = ""
        self.data['alternatives-1-title'] = ""
        self.data['alternatives-2-title'] = ""

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_two_alternatives(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-0-title'] = ""
        self.data['alternatives-1-title'] = ""

        self.verify_field_error_validation(self.data)

    def test_create_question_fail_three_alternatives(self):
        """
        User can not create a question with invalid fields and alternativas.
        """

        self.data['alternatives-0-title'] = ""

        self.verify_field_error_validation(self.data)

    def verify_create_question_ok(self):
        """
        Verify that the creation is correct
        """

        response = self.client.post(self.url, self.data, follow=True)
        self.assertRedirects(response, self.redirect_url)
        self.question.refresh_from_db()
        for alternative in self.alternatives:
            alternative.refresh_from_db()
        self.assertIsNotNone(response.context_data)
        self.assertEqual(self.question.title, self.data['title'])
        self.assertEqual(self.alternatives[0].title, self.data['alternatives-0-title'])
        self.assertEqual(self.alternatives[0].is_correct, False)
        self.assertEqual(self.alternatives[2].title, self.data['alternatives-2-title'])
        self.assertEqual(self.alternatives[2].is_correct, True)
        check_messages(
            self, response,
            tag='alert-success',
            content='Question updated successfully.'
        )

    def verify_field_error_validation(self, data):
        """
        Verify field error validation.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.question.refresh_from_db()
        for alternative in self.alternatives:
            alternative.refresh_from_db()
        self.assertEqual(self.question.title, "Question")
        self.assertEqual(self.alternatives[0].title, "Alternative")
        self.assertEqual(self.alternatives[0].is_correct, True)
        self.assertEqual(self.alternatives[2].title, "Alternative")
        self.assertEqual(self.alternatives[2].is_correct, False)

        return response