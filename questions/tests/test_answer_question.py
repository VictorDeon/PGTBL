from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from model_mommy import mommy
from questions.models import (Question, Alternative, ExerciseSubmission)
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

        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@gmail.com',
            password='test1234',
            is_teacher=True,
        )
        self.session.discipline.teacher = self.teacher
        self.session.discipline.save()

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
        Alternative.objects.all().delete()

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

    def test_result_answer_validation_for_wrong_scores(self):
        """
        The result need to be between 0 and 4 points.
        """

        """
        Cannot test the error message, bacause it is passed throught
        _request attribute, which it is not the best solution and
        the status code for the response is always 302, even when occur errors
        """
        self.client.login(username=self.student.username, password='test1234')

        data = {
            'alternative01-score': 1,
            'alternative02-score': 1,
            'alternative03-score': 4,
            'alternative04-score': 4,
        }

        self.client.post(self.url_submit_answer, data=data)
        self.assertEqual(ExerciseSubmission.objects.all().count(), 0)

    def test_result_answer_validation_for_right_scores(self):
        """
        The result need to be between 0 and 4 points.
        """
        self.client.login(username=self.student.username, password='test1234')

        data = {
            'alternative01-score': 1,
            'alternative02-score': 1,
            'alternative03-score': 1,
            'alternative04-score': 1,
        }

        self.client.post(self.url_submit_answer, data=data)
        self.assertEqual(ExerciseSubmission.objects.all().count(), 1)

    def test_only_submit_one_time(self):
        """
        User can only submit a answer once.
        """
        """
        Cannot test the error message, bacause it is passed throught
        _request attribute, which it is not the best solution and
        the status code for the response is always 302, even when occur errors
        """
        self.client.login(username=self.student.username, password='test1234')

        data = {
            'alternative01-score': 1,
            'alternative02-score': 1,
            'alternative03-score': 1,
            'alternative04-score': 1,
        }

        self.client.post(self.url_submit_answer, data=data)
        self.client.post(self.url_submit_answer, data=data)
        self.assertEqual(ExerciseSubmission.objects.all().count(), 1)
