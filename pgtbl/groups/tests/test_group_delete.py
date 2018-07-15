from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import Discipline
from groups.models import Group

User = get_user_model()


class GroupDeleteTestCase(TestCase):
    """
    Test to delete a new group by teacher.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234'
        )
        self.monitor = User.objects.create_user(
            username='Test2',
            email='test2@gmail.com',
            password='test1234'
        )
        self.student = User.objects.create_user(
            username='Test3',
            email='test3@gmail.com',
            password='test1234',
            is_teacher=False
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline',
            course='Engineering',
            password='12345',
            students_limit=5,
            monitors_limit=2,
            students=[self.student],
            monitors=[self.monitor],
            make_m2m=True
        )
        self.group = mommy.make(
            Group,
            discipline=self.discipline,
            title='Group01',
            students_limit=3,
            students=[self.student],
        )
        self.url = reverse_lazy(
            'groups:delete',
            kwargs={'slug': self.discipline.slug, 'pk': self.group.id}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.teacher.delete()
        self.monitor.delete()
        self.student.delete()

    def test_delete_group_ok(self):
        """
        Test to delete a new group with success.
        """

        self.assertEqual(self.discipline.groups.count(), 1)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        url = reverse_lazy(
            'groups:list',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, url)
        self.assertEqual(self.discipline.groups.count(), 0)
        check_messages(
            self, response,
            tag='alert-success',
            content="Group deleted successfully."
        )

    def test_delete_group_by_student(self):
        """
        Student can't delete a group.
        """

        self.assertEqual(self.discipline.groups.count(), 1)
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, url)
        self.assertEqual(self.discipline.groups.count(), 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_delete_group_by_monitor(self):
        """
        Monitor can't delete a group.
        """

        self.assertEqual(self.discipline.groups.count(), 1)
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, url)
        self.assertEqual(self.discipline.groups.count(), 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
