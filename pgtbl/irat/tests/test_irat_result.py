from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from grades.models import Grade
from groups.models import Group
from irat.models import IRATSubmission
from modules.models import TBLSession
from questions.models import Question, Alternative

User = get_user_model()


class IRATResultTestCase(TestCase):
    """
    Test to show iRAT result.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.teacher_monitor = user_factory(name="otavio", is_teacher=True)
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
            monitors=[self.monitor, self.teacher_monitor]
        )
        self.group = mommy.make(
            Group,
            discipline=self.discipline,
            title="Grupo 01",
            students_limit=4,
            students=[self.student]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            irat_datetime=timezone.now() - timedelta(minutes=35),
            irat_duration=10,
            grat_datetime=timezone.now() - timedelta(minutes=20),
            grat_duration=10,
            is_closed=False
        )
        self.questions = mommy.make(
            Question,
            title="Question",
            topic="Topic",
            level='Basic',
            is_exercise=False,
            session=self.module,
            _quantity=3
        )
        self.submission1 = mommy.make(
            IRATSubmission,
            session=self.module,
            question=self.questions[0],
            user=self.student,
            correct_alternative="Alternative 01",
            score=4
        )
        self.submission2 = mommy.make(
            IRATSubmission,
            session=self.module,
            question=self.questions[1],
            user=self.student,
            correct_alternative="Alternative 03",
            score=3
        )
        self.submission3 = mommy.make(
            IRATSubmission,
            session=self.module,
            question=self.questions[2],
            user=self.student,
            correct_alternative="Alternative 01",
            score=2
        )
        self.redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'irat:result',
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
        IRATSubmission.objects.all().delete()

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
        self.assertTemplateUsed(response, 'irat/result.html')

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

    def test_teacher_can_see_the_irat_result(self):
        """
        Teacher can see the iRAT result
        with exercises questions answered.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_the_closed_session_irat_result(self):
        """
        Teacher can see the iRAT result when session is closed
        with exercises questions answered.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_the_irat_result_if_grat_not_finished(self):
        """
        Teacher can see the iRAT result if gRAT is not finished.
        """

        # Now 10:00, grat 9:40, gRAt finish 10:10
        self.module.grat_duration = 30
        self.module.save()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_can_see_the_irat_result(self):
        """
        Student can see the iRAT result
        with exercises questions answered.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_can_not_see_the_closed_session_irat_result(self):
        """
        Student can not see the iRAT result when session is closed
        with exercises questions answered.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_student_can_not_see_the_irat_result_if_grat_not_finished(self):
        """
        Student can not see the iRAT result if gRAT is not finished.
        """

        # Now 10:00, grat 9:40, gRAt finish 10:10
        self.module.grat_duration = 30
        self.module.save()
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path, status_code=302, target_status_code=200)
        
    def test_calcule_student_irat_result(self):
        """
        Calcule the iRAT result from iRAT list.
        score that the student made, total of scores
        and create a Grade.
        """

        result = {
            'score': 9,  # sum of submissions score
            'total': 12,  # 4 * number of questions
            'grade': "7.50"  # (score/total) * 10
        }
        self.assertEqual(Grade.objects.count(), 0)
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(Grade.objects.count(), 1)
        self.assertTrue('result' in response.context)
        self.assertEqual(response.context['result'], result)

    def test_not_calcule_teacher_irat_result(self):
        """
        Calcule the iRAT result from iRAT list.
        score that the teacher made, total of scores
        but not create a Grade.
        """

        result = {
            'score': 0,  # sum of submissions score
            'total': 12,  # 4 * number of questions
            'grade': "0.00"  # (score/total) * 10
        }
        self.assertEqual(Grade.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(Grade.objects.count(), 0)
        self.assertTrue('result' in response.context)
        self.assertEqual(response.context['result'], result)

    def test_not_calcule_monitor_teacher_irat_result(self):
        """
        Calcule the iRAT result from iRAT list.
        score that the monitor teacher made, total of scores
        but not create a Grade.
        """

        result = {
            'score': 0,  # sum of submissions score
            'total': 12,  # 4 * number of questions
            'grade': "0.00"  # (score/total) * 10
        }
        self.assertEqual(Grade.objects.count(), 0)
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(Grade.objects.count(), 0)
        self.assertTrue('result' in response.context)
        self.assertEqual(response.context['result'], result)

    def test_not_calculate_monitor_irat_result(self):
        """
        Calcule the iRAT result from iRAT list.
        score that the monitor made, total of scores
        but not create a Grade.
        """

        result = {
            'score': 0,  # sum of submissions score
            'total': 12,  # 4 * number of questions
            'grade': "0.00"  # (score/total) * 10
        }
        self.assertEqual(Grade.objects.count(), 0)
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(Grade.objects.count(), 0)
