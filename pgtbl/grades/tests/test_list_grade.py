from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages, user_factory
from model_mommy import mommy

from disciplines.models import Discipline
from grades.models import Grade, FinalGrade
from groups.models import Group
from modules.models import TBLSession

User = get_user_model()


class ListGradeTestCase(TestCase):
    """
    Test to list session grades.
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
        self.group = mommy.make(
            Group,
            discipline=self.discipline,
            title="Grupo teste",
            students_limit=10,
            students=[self.student]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            is_closed=False,
            peer_review_weight=1
        )
        self.grade = mommy.make(
            Grade,
            session=self.module,
            student=self.student,
            group=self.group,
            irat=8.0,
            grat=10.0,
            practical=6.5,
            peer_review=8
        )
        self.url = reverse_lazy(
            'grades:list',
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
        self.grade.delete()

    def test_redirect_to_login(self):
        """
        User can not see the grade list without logged in.
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
        self.assertTemplateUsed(response, 'grades/list.html')
        self.assertEqual(Grade.objects.count(), 1)

    def test_context(self):
        """
        Test to get all context from page.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('irat_datetime' in response.context)
        self.assertTrue('grat_datetime' in response.context)
        self.assertTrue('discipline' in response.context)
        self.assertTrue('session' in response.context)
        self.assertTrue('grades' in response.context)
        self.assertTrue('date' in response.context)

    def test_student_can_see_the_grades(self):
        """
        User students can see the list of grades.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monitor_can_see_the_grades(self):
        """
        User monitor can see the list of grades.
        """

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_monitor_can_see_the_grades(self):
        """
        User teacher monitor can see the list of grades.
        """

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_the_grades(self):
        """
        User teacher can see the list of grades.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_calculate_session_grade(self):
        """
        Unit test about calculate_session_grade() method from Grade model.
        iRAT = 8,0 * 3 = 24
        gRAT = 10,0 * 2 = 20
        practical = 6,5 * 4 = 26
        peer_review = 8 * 1 = 8
        total = 78/10 = 7,8
        """

        self.assertEqual(self.grade.calcule_session_grade(), 7.8)

    def test_calculate_session_grade_without_peer_review(self):
        """
        Unit test about calculate_session_grade() method from Grade model.
        iRAT = 8,0 * 3 = 24
        gRAT = 10,0 * 3 = 30
        practical = 6,5 * 4 = 26
        total = 80/10 = 8
        """

        self.module.peer_review_weight = 0
        self.module.grat_weight = 3
        self.module.save()
        self.assertEqual(self.grade.calcule_session_grade(), 8)