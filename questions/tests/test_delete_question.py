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
        self.session = mommy.make('TBLSession')

        self.question = mommy.make(
            Question,
            title='testtitle',
            session= self.session,
            level= 'basic',
            topic= 'testtopic',
        )


        self.alternatives = mommy.make('Alternative', _quantity=4)
        self.alternatives[0].is_correct = True
        self.alternatives[0].save()
        self.question.alternatives.set(self.alternatives)
        self.session.questions.add(self.question)


        self.student = User.objects.create_user(
            username='Test3',
            email='test3@gmail.com',
            password='test1234',
            is_teacher=False
        )

        self.session.discipline.students.add(self.student)

        self.teacher = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234',
            is_teacher=True
        )

        self.session.discipline.teacher = self.teacher

        self.monitor = User.objects.create_user(
            username='Test2',
            email='test2@gmail.com',
            password='test1234',
            is_teacher=True
        )

        self.session.discipline.monitors.add(self.monitor)
        self.session.discipline.save()

        self.url = reverse_lazy(
            'questions:delete-question',
            kwargs={'slug': self.session.
                    discipline.slug,
                    'pk': self.session.pk,
                    'question_id':self.question.id}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        # self.teacher.delete()
        # self.monitor.delete()
        # self.student.delete()
        # self.question.delete()

        User.objects.all().delete()
        Question.objects.all().delete()
        TBLSession.objects.all().delete()
        Alternative.objects.all().delete()


    def test_redirect_to_login(self):
        """
        User can not delete a question without logged in.
        """

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_delete_question_by_teacher(self):
        """
        Test to delete a question by teacher.
        """
        self.assertEqual(self.session.questions.count(), 1)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url)
        self.assertEqual(self.session.questions.count(), 0)

    def test_delete_question_by_monitors(self):
        """
        Test to delete a question by monitors.
        """
        self.assertEqual(self.session.questions.count(), 1)
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.post(self.url)
        self.assertEqual(self.session.questions.count(), 0)

    def test_delete_question_by_student_fail(self):
        """
        Student can not delete a question.
        """

        self.assertEqual(self.session.questions.count(),1)
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url)
        self.assertEqual(self.session.questions.count(), 1)

    def test_delete_alternatives_when_delete_question(self):
        """
        Test to delete all alternatives when delete a specific question.
        """

        self.assertEqual(self.session.questions.count(),1)
        self.assertEqual(Alternative.objects.all().count(), 4)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url)
        self.assertEqual(self.session.questions.count(), 0)
        self.assertEqual(Alternative.objects.all().count(), 0)

