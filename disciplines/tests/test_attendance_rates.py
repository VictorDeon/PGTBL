from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline, Attendance, AttendanceRate
from model_mommy import mommy
from core.test_utils import (
    check_messages, user_factory
)

User = get_user_model()


class AttendanceTestCase(TestCase):
    """
    Test case insert students in attendance list
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro', password='test1234')
        self.students = user_factory(
            qtd=9,
            is_teacher=False
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline04',
            course='Engineering',
            password='12345',
            is_closed=True,
            students_limit=10,
            students=self.students,
            make_m2m=True
        )
        self.client.login(username=self.teacher.username, password='test1234')
        self.attendance = mommy.make(
            Attendance,
            date='2018-10-10',
            discipline=self.discipline,
            attended_students=self.students,
        )
        self.url = reverse_lazy(
            'disciplines:attendance',
            kwargs={'slug': self.discipline.slug}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        Discipline.objects.all().delete()
        Attendance.objects.all().delete()
        User.objects.all().delete()
        self.client.logout()
        AttendanceRate.objects.all().delete()

    def test_create_att_rate(self):
        """
        This method will test if an attendance rate was succesfully created
        with all students in the class
        """

        self.client.get(self.url)
        self.assertEqual(AttendanceRate.objects.count(), 9)

    def test_check_attended_students(self):
        """
        This method will test if the attendance rate has listed
        correctly attended and missed students
        """

        self.client.get(self.url)
        rates = AttendanceRate.objects.filter(
                    discipline=self.discipline
                )

        for rate in rates:
            self.assertNotEqual(rate.times_attended, 0)