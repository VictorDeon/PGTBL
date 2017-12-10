from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    list_transform, check_messages, user_factory
)

User = get_user_model()


class ChangeStudentTestCase(TestCase):
    """
    Tests to change student to monitor or monitor to student.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.student = user_factory(name='João', is_teacher=False)
        self.monitor = user_factory(name="Maria")
        self.students = user_factory(qtd=4, is_teacher=False)
        self.monitors = user_factory(qtd=2)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline04',
            course='Engineering',
            password='12345',
            students_limit=10,
            monitors_limit=3,
            students=self.students,
            monitors=self.monitors,
            make_m2m=True
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        Discipline.objects.all().delete()
        User.objects.all().delete()

    def test_number_of_students_and_monitors(self):
        """
        Test number of students and monitors.
        """

        self.assertEqual(self.discipline.students.count(), 4)
        self.assertEqual(self.discipline.monitors.count(), 2)

    def test_change_student_to_monitor_and_monitor_to_student(self):
        """
        Test to change student to monitor by teacher.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        url = reverse_lazy(
            'disciplines:change-student',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.students[0].id
            }
        )
        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
        self.verify_change(
            url, redirect_url,
            'alert-success',
            'Successful modification'
        )
        self.assertEqual(self.discipline.students.count(), 3)
        self.assertEqual(self.discipline.monitors.count(), 3)

        self.verify_change(
            url, redirect_url,
            'alert-success',
            'Successful modification'
        )
        self.assertEqual(self.discipline.students.count(), 4)
        self.assertEqual(self.discipline.monitors.count(), 2)

    def test_can_not_change_monitor_if_is_teacher(self):
        """
        Test can't change monitor to student if monitor is a teacher.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        url = reverse_lazy(
            'disciplines:change-student',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.monitors[0].id
            }
        )
        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
        self.verify_change(
            url, redirect_url,
            'alert-danger',
            "You can't turn a teacher into a student."
        )
        self.assertEqual(self.discipline.students.count(), 4)
        self.assertEqual(self.discipline.monitors.count(), 2)

    def verify_change(self, url, redirect_url, tag, content):
        """
        Verify if changed.
        """

        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url)
        check_messages(
            self, response,
            tag=tag,
            content=content
        )

    def test_student_can_not_change_youself_to_monitor(self):
        """
        Test can't student change yourself to monitor.
        """

        self.verify_change_fail(self.students[0], self.monitors[0])

    def test_student_can_not_change_other_student_to_monitor(self):
        """
        Test student can't change other student to monitor.
        """

        self.verify_change_fail(self.students[0], self.monitors[1])

    def test_student_can_not_change_monitor_to_student(self):
        """
        Test student can't change monitor to student.
        """

        self.verify_change_fail(self.students[0], self.monitors[0])

    def test_monitor_can_not_change_yourself_to_student(self):
        """
        Test monitor can't change yourself to student
        """

        self.verify_change_fail(self.monitors[0], self.monitors[0])

    def test_monitor_can_not_change_other_monitor_to_student(self):
        """
        Test monitor can't change other monitor to student.
        """

        self.verify_change_fail(self.monitors[0], self.monitors[1])

    def test_monitor_can_not_change_student_to_monitor(self):
        """
        Test monitor can't change student to monitor.
        """

        self.verify_change_fail(self.monitors[0], self.students[0])

    def test_teacher_outside_discipline(self):
        """
        Teacher outside discipline can't change monitor or students from
        discipline.
        """

        self.verify_change_fail(self.monitor, self.students[0])

    def test_student_outside_discipline(self):
        """
        Teacher outside discipline can't change monitor or students from
        discipline.
        """

        self.verify_change_fail(self.student, self.students[0])

    def verify_change_fail(self, logged_user, user):
        """
        Verify change fail and redirect to profile.
        """

        self.client.login(
            username=logged_user.username,
            password='test1234'
        )
        url = reverse_lazy(
            'disciplines:change-student',
            kwargs={
                'slug': self.discipline.slug,
                'pk': user.id
            }
        )
        redirect_url = reverse_lazy('accounts:profile')
        self.verify_change(
            url, redirect_url,
            'alert-danger',
            "You are not authorized to do this action."
        )
        self.assertEqual(self.discipline.students.count(), 4)
        self.assertEqual(self.discipline.monitors.count(), 2)
