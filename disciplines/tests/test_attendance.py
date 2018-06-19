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
        self.teachers = user_factory(qtd=2)
        self.student = user_factory(name='Maria', is_teacher=False)
        self.monitor = user_factory(name='Caio')
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
            monitors_limit=3,
            students=self.students,
            monitors=self.teachers,
            make_m2m=True
        )
        self.client.login(username=self.teacher.username, password='test1234')
        self.url = reverse_lazy(
            'disciplines:createNewAttendance',
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

    def get_attendance(self, discipline, date):
        
        attendance = Attendance.objects.get(
                        discipline=discipline,
                        date=date
                    )

        return attendance

    def test_create_attendance(self):
        """
        This method will test if an attendance was succesfully created 
        """

        students_pk = []

        for student in self.students:
            students_pk.append(student.pk)

        data = {
            'students':students_pk,
            'date':'2018-10-10'
        }

        self.client.post(self.url, data)

        self.assertEqual(Attendance.objects.count(), 1)

    def test_attended_not_in_missed(self):
        """
        This method will test if a attended student is listed in missed students
        """

        students_pk = []

        for i in range(0,6):
            students_pk.append(self.students[i].pk)

        data = {
            'students':students_pk,
            'date':'2018-10-10'
        }

        response = self.client.post(self.url, data)
        attendance = self.get_attendance(self.discipline, data['date'])

        self.assertEqual(Attendance.objects.count(), 1)
        self.assertNotIn(attendance.attended_students.all(), attendance.missing_students.all())
        self.assertNotIn(attendance.missing_students.all(), attendance.attended_students.all())

    def test_edit_attendance(self):
        """
        This method will test if a missing student marked as
        attended, after certain attendance is edited, will still
        be listed in missing students
        """

        students_pk = []
        students_pk_after_edit = []

        for i in range(0,6):
            students_pk.append(self.students[i].pk)

        for student in self.students:
            students_pk_after_edit.append(student.pk)

        data = {
            'students':students_pk,
            'date':'2018-10-10'
        }

        data_edit = {
            'students':students_pk_after_edit,
            'date':'2018-10-10'
        }

        response = self.client.post(self.url, data)
        response = self.client.post(self.url, data_edit)
        attendance = self.get_attendance(self.discipline, data['date'])

        self.assertNotIn(attendance.attended_students.all(), attendance.missing_students.all())
        self.assertNotIn(attendance.missing_students.all(), attendance.attended_students.all())
        self.assertEqual(attendance.attended_students.all().count(), 9)
        self.assertEqual(attendance.missing_students.all().count(), 0)
