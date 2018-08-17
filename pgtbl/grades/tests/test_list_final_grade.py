from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.test import TestCase, Client
from core.test_utils import user_factory
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
        self.module1 = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            is_closed=False,
            peer_review_weight=1
        )
        self.grade1 = mommy.make(
            Grade,
            session=self.module1,
            student=self.student,
            group=self.group,
            irat=8.0,
            grat=10.0,
            practical=6.5,
            peer_review=8
        )
        self.module2 = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            is_closed=False,
            peer_review_weight=0,
            grat_weight=3
        )
        self.grade2 = mommy.make(
            Grade,
            session=self.module2,
            student=self.student,
            group=self.group,
            irat=6.0,
            grat=8.5,
            practical=7.3
        )
        self.grade = mommy.make(
            FinalGrade,
            discipline=self.discipline,
            student=self.student
        )
        self.url = reverse_lazy(
            'grades:result',
            kwargs={'slug': self.discipline.slug}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.module1.delete()
        self.module2.delete()
        self.grade1.delete()
        self.grade2.delete()
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
        self.assertTemplateUsed(response, 'grades/result.html')
        self.assertEqual(FinalGrade.objects.count(), 1)

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
        self.assertTrue('discipline' in response.context)
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

    def test_calcule_final_grade(self):
        """
        Unit test about calculate_session_grade() method from Grade model.
        SESSÃO 01:
        iRAT1 = 8,0 * 3 = 24
        gRAT1 = 10,0 * 2 = 20
        practical1 = 6,5 * 4 = 26
        peer_review1 = 8 * 1 = 8
        total1 = 78/10 = 7,80

        SESSÃO 02:
        iRAT2 = 6,0 * 3 = 18
        gRAT2 = 8,5 * 3 = 25,5
        practical2 = 7,3 * 4 = 29,2
        total2 = 72,7/10 = 7,27

        total = (7,80 + 7,27)/2 = 7,53
        status = Approved
        """

        self.assertEqual(self.grade.calcule_final_grade(), 7.535)

    def test_save_the_status_and_final_grade(self):
        """
        Save the status and final grade when go to final grade table url.
        """

        self.client.login(username=self.student.username, password='test1234')
        self.client.get(self.url)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.final_grade, 7.535)
        self.assertEqual(self.grade.status, _("Approved"))