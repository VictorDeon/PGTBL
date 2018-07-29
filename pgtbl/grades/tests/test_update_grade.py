from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages, user_factory
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy

from disciplines.models import Discipline
from grades.models import Grade
from groups.models import Group
from modules.models import TBLSession

User = get_user_model()


class UpdateGradeTestCase(TestCase):
    """
    Test to update a specific grade from a specific student.
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
            'grades:update',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk,
                'student_pk': self.student.pk
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

    def test_update_grade_by_teacher(self):
        """
        Test to update a grade by teacher.
        """

        self.client.login(username=self.teacher.username, password="test1234")
        data = {'irat': 9.5, 'grat': 10.0, 'practical': 6.5, 'peer_review': 8}
        response = self.client.post(self.url, data, follow=True)
        grades_url = reverse_lazy(
            'grades:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.assertRedirects(response, grades_url)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.irat, data['irat'])
        check_messages(
            self, response,
            tag='alert-success',
            content='Grades updated successfully.'
        )

    def test_not_update_grade_by_monitors(self):
        """
        Test to not update a grade by monitors.
        """

        self.client.login(username=self.monitor.username, password="test1234")
        data = {'irat': 9.5, 'grat': 10.0, 'practical': 6.5, 'peer_review': 8}
        response = self.client.post(self.url, data, follow=True)
        failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.assertRedirects(response, failure_redirect_path)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.irat, 8.0)
        check_messages(
            self, response,
            tag='alert-danger',
            content='You are not authorized to do this action.'
        )

    def test_not_update_grade_by_monitor_teacher(self):
        """
        Test to not update a grade by teacher monitors.
        """

        self.client.login(username=self.teacher_monitor.username, password="test1234")
        data = {'irat': 9.5, 'grat': 10.0, 'practical': 6.5, 'peer_review': 8}
        response = self.client.post(self.url, data, follow=True)
        failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.assertRedirects(response, failure_redirect_path)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.irat, 8.0)
        check_messages(
            self, response,
            tag='alert-danger',
            content='You are not authorized to do this action.'
        )

    def test_update_grade_by_student_fail(self):
        """
        Student can not update a grade.
        """

        self.client.login(username=self.student.username, password="test1234")
        data = {'irat': 9.5, 'grat': 10.0, 'practical': 6.5, 'peer_review': 8}
        response = self.client.post(self.url, data, follow=True)
        failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.assertRedirects(response, failure_redirect_path)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.irat, 8.0)
        check_messages(
            self, response,
            tag='alert-danger',
            content='You are not authorized to do this action.'
        )

    def test_update_grade_fail_bigger(self):
        """
        Teacher can not update a grade with invalid fields.
        The grade need to be bigger than 0 and smaller than 10.
        """

        self.client.login(username=self.teacher.username, password="test1234")
        data = {'irat': 9.5, 'grat': 11.0, 'practical': 6.5, 'peer_review': 8}
        response = self.client.post(self.url, data, follow=True)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.grat, 10.0)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Grade need to be a number between 0 and 10.'
        )

    def test_update_grade_fail_smaller(self):
        """
        Teacher can not update a grade with invalid fields.
        The grade need to be bigger than 0 and smaller than 10.
        """

        self.client.login(username=self.teacher.username, password="test1234")
        data = {'irat': 9.5, 'grat': -7.0, 'practical': 6.5, 'peer_review': 8}
        response = self.client.post(self.url, data, follow=True)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.grat, 10.0)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Grade need to be a number between 0 and 10.'
        )
