from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from grat.models import GRATSubmission
from groups.models import Group
from modules.models import TBLSession
from questions.models import Question, Alternative

User = get_user_model()


class ListGRATTestCase(TestCase):
    """
    Test to list question into gRAT.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.student = user_factory(name="joao", is_teacher=False)
        self.student_no_group = user_factory(name="otavio", is_teacher=False)
        self.student_same_group = user_factory(name="otavio", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student, self.student_no_group, self.student_same_group],
            monitors=[self.monitor]
        )
        self.group = mommy.make(
            Group,
            discipline=self.discipline,
            title="Group test",
            students_limit=4,
            students=[self.student, self.student_same_group]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            irat_datetime=timezone.now() - timedelta(minutes=31),
            grat_datetime=timezone.now(),
            is_closed=False
        )
        self.question = mommy.make(
            Question,
            title="Question",
            topic="Topic",
            level='Basic',
            is_exercise=False,
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
        self.redirect_url = reverse_lazy(
            'grat:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'grat:answer-question',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk,
                'question_id': self.question.pk,
                'question_page': "1"
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

    def test_correct_answer_student_no_group(self):
        """
        Test to get the get an message error if student is not inside into a group.
        """

        data = {
            'alternative01-score': 4,
            'alternative02-score': 2,
            'alternative03-score': 1,
            'alternative04-score': 0
        }

        self.client.login(username=self.student_no_group.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="Student must be in a group to answer the test."
        )

    def test_correct_answer_ok(self):
        """
        Test to get the correct answer and create a submission with four points
        in the question
        """

        data = {
            'alternative01-score': 4,
            'alternative02-score': 2,
            'alternative03-score': 1,
            'alternative04-score': 0
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(4, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question answered successfully."
        )

    def test_two_points_correct_answer(self):
        """
        Test to get the correct answer and create a submission with two points
        in the question
        """

        data = {
            'alternative01-score': 2,
            'alternative02-score': 4,
            'alternative03-score': 1,
            'alternative04-score': 0
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(2, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question answered successfully."
        )

    def test_one_points_correct_answer(self):
        """
        Test to get the correct answer and create a submission with two points
        in the question
        """

        data = {
            'alternative01-score': 1,
            'alternative02-score': 2,
            'alternative03-score': 4,
            'alternative04-score': 0
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(1, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question answered successfully."
        )

    def test_zero_points_correct_answer(self):
        """
        Test to get the correct answer and create a submission with two points
        in the question
        """

        data = {
            'alternative01-score': 0,
            'alternative02-score': 4,
            'alternative03-score': 2,
            'alternative04-score': 1
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(0, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question answered successfully."
        )

    def test_alternative_answer_bigger_than_four(self):
        """
        Test to verify if can insert more than four points
        """

        data = {
            'alternative01-score': 4,
            'alternative02-score': 2,
            'alternative03-score': 1,
            'alternative04-score': 4
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You can't repeat the options."
        )

    def test_alternative_answer_incorrect_input(self):
        """
        Test to verify if can insert more than four points
        """

        data = {
            'alternative01-score': 4,
            'alternative02-score': 4,
            'alternative03-score': 4,
            'alternative04-score': 4
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You can't repeat the options."
        )

    def test_can_not_submit_twice_if_same_group(self):
        """
        Same question can not be submited twice.
        """

        data = {
            'alternative01-score': 2,
            'alternative02-score': 4,
            'alternative03-score': 1,
            'alternative04-score': 0
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(2, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question answered successfully."
        )
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(2, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-danger',
            content="Your group has already answered this question."
        )
        self.client.login(username=self.student_same_group.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_url + "?page=1")
        self.assertEqual(GRATSubmission.objects.count(), 1)
        self.assertEqual(2, GRATSubmission.objects.first().score)
        check_messages(
            self, response,
            tag='alert-danger',
            content="Your group has already answered this question."
        )