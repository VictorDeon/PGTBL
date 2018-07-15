from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import Discipline
from groups.models import Group

User = get_user_model()


class GroupListTestCase(TestCase):
    """
    Test to list all groups.
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
        self.groups = mommy.make(
            Group,
            discipline=self.discipline,
            _quantity=7,
        )
        self.url = reverse_lazy(
            'groups:list',
            kwargs={'slug': self.discipline.slug}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.teacher.delete()
        self.monitor.delete()
        self.student.delete()
        Group.objects.all().delete()

    def test_redirect_to_login(self):
        """
        Try to access group list without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_group_pagination(self):
        """
        Test to show groups pagination.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        paginator = response.context['paginator']
        groups = response.context['groups']
        # Total number of objects, across all pages.
        self.assertEqual(paginator.count, 7)
        # The maximum number of items to include on a page.
        self.assertEqual(paginator.per_page, 5)
        # Total number of pages.
        self.assertEqual(paginator.num_pages, 2)
        # Number of disciplines opened
        self.assertEqual(groups.count(), 5)

    def test_teacher_change_group_permission(self):
        """
        Test teacher change the group permission.
        """

        self.assertEqual(self.discipline.was_group_provided, False)
        self.client.login(username=self.teacher.username, password='test1234')
        url = reverse_lazy(
            'groups:provide',
            kwargs={'slug': self.discipline.slug}
        )
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, self.url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.was_group_provided, True)
        check_messages(
            self, response,
            tag='alert-success',
            content="Groups available."
        )

    def test_student_can_not_change_group_permission(self):
        """
        Test student can't change the group permission.
        """

        self.assertEqual(self.discipline.was_group_provided, False)
        self.client.login(username=self.student.username, password='test1234')
        url = reverse_lazy(
            'groups:provide',
            kwargs={'slug': self.discipline.slug}
        )
        response = self.client.post(url, follow=True)
        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, redirect_url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.was_group_provided, False)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_monitor_can_not_change_group_permission(self):
        """
        Test monitor can't change the group permission.
        """

        self.assertEqual(self.discipline.was_group_provided, False)
        self.client.login(username=self.monitor.username, password='test1234')
        url = reverse_lazy(
            'groups:provide',
            kwargs={'slug': self.discipline.slug}
        )
        response = self.client.post(url, follow=True)
        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, redirect_url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.was_group_provided, False)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_students_can_not_see_the_groups(self):
        """
        Test only teacher can see the groups before release it.
        """

        self.assertEqual(self.discipline.was_group_provided, False)
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, redirect_url)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_monitor_can_not_see_the_groups(self):
        """
        Test only teacher can see the groups before release it.
        """

        self.assertEqual(self.discipline.was_group_provided, False)
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse_lazy(
            'disciplines:details',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, redirect_url)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_students_can_see_the_groups(self):
        """
        Test students can see the groups after teacher release it.
        """

        self.discipline.was_group_provided = True
        self.discipline.save()
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/list.html')

    def test_monitors_can_see_the_groups(self):
        """
        Test monitors can see the groups after teacher release it.
        """

        self.discipline.was_group_provided = True
        self.discipline.save()
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/list.html')
