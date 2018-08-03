from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from exercises.models import ExerciseSubmission
from modules.models import TBLSession
from questions.models import Question, Alternative

User = get_user_model()


class ExerciseResultTestCase(TestCase):
    """
    Test to show exercises result.
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
            description="Description test",
            is_closed=False
        )
        self.questions = mommy.make(
            Question,
            title="Question",
            topic="Topic",
            level='Basic',
            is_exercise=True,
            session=self.module,
            _quantity=3
        )
        self.submission1 = mommy.make(
            ExerciseSubmission,
            session=self.module,
            question=self.questions[0],
            user=self.student,
            correct_alternative="Alternative 01",
            score=4
        )
        self.submission2 = mommy.make(
            ExerciseSubmission,
            session=self.module,
            question=self.questions[1],
            user=self.student,
            correct_alternative="Alternative 03",
            score=3
        )
        self.submission3 = mommy.make(
            ExerciseSubmission,
            session=self.module,
            question=self.questions[2],
            user=self.student,
            correct_alternative="Alternative 01",
            score=2
        )
        self.url = reverse_lazy(
            'exercises:result',
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
        ExerciseSubmission.objects.all().delete()

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_status_code_200(self):
        """
        Test status code and templates.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exercises/result.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertTrue('date' in response.context)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('irat_datetime' in response.context)
        self.assertTrue('grat_datetime' in response.context)
        self.assertTrue('discipline' in response.context)
        self.assertTrue('session' in response.context)
        self.assertTrue('result' in response.context)
        self.assertTrue('submissions' in response.context)

    def test_teacher_can_see_the_exercise_result(self):
        """
        Teacher can see the exercises result
        with exercises questions answered.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_the_closed_session_exercise_result(self):
        """
        Teacher can see the exercises result when session is closed
        with exercises questions answered.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monitor_can_see_the_exercise_result(self):
        """
        Monitor can see the exercises result
        with exercises questions answered.
        """

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monitor_can_see_the_closed_session_exercise_list(self):
        """
        Monitor can see the exercises result when the session is closed
        with exercises questions answered.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_can_see_the_exercise_result(self):
        """
        Student can see the exercises result
        with exercises questions answered.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_can_not_see_the_closed_session_exercise_result(self):
        """
        Student can not see the exercises result when session is closed
        with exercises questions answered.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))

    def test_user_can_not_see_the_exercise_result(self):
        """
        User that is not into discipline can't see the exercises result
        with exercises questions answered.
        """

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))

    def test_calcule_the_exercise_result(self):
        """
        Calcule the exercises result from exercises list.
        score that the user made, total of scores and grade of user.
        """

        result = {
            'score': 9,  # sum of submissions score
            'total': 12,  # 4 * number of questions
            'grade': "7.50"  # (score/total) * 10
        }
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertTrue('result' in response.context)
        self.assertEqual(response.context['result'], result)

    def test_reset_exercise_list(self):
        """
        Remove all submissions from exercises list.
        """

        url = reverse_lazy(
            'exercises:reset',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        redirect_url = reverse_lazy(
            'exercises:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.client.login(username=self.student.username, password='test1234')
        self.assertEqual(ExerciseSubmission.objects.count(), 3)
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(ExerciseSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-success',
            content="Exercise list reseted successfully."
        )
