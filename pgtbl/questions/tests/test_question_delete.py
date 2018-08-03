from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession
from questions.models import Question, Alternative

User = get_user_model()


class DeleteQuestionTestCase(TestCase):
    """
    Test to delete a question.
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
        self.redirect_url = reverse_lazy(
            'exercises:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'questions:delete-question',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk,
                'question_id': self.question.pk
            }
        )
        self.redirect_url = reverse_lazy(
            'exercises:list',
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

    def test_delete_question_by_teacher(self):
        """
        Test to delete a question by teacher.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question deleted successfully."
        )

    def test_delete_question_by_monitors(self):
        """
        Test to delete a question by monitors.
        """

        self.client.login(username=self.monitor.username, password='test1234')
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Alternative.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-success',
            content="Question deleted successfully."
        )

    def test_delete_question_by_student_fail(self):
        """
        Student can not delete a question.
        """

        self.client.login(username=self.student.username, password='test1234')
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_delete_question_by_user_fail(self):
        """
        User that is not into discipline can not delete a question.
        """

        self.client.login(username=self.user.username, password='test1234')
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Alternative.objects.count(), 4)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
