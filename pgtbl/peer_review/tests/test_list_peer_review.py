from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession

User = get_user_model()


class ListPeerReviewTestCase(TestCase):
    """
    Test to list Peer Review
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.teacher_monitor = user_factory(name="otavio", is_teacher=True)
        self.student1 = user_factory(name="joao", is_teacher=False)
        self.student2 = user_factory(name="victor", is_teacher=False)
        self.student3 = user_factory(name="jean", is_teacher=False)
        self.student4 = user_factory(name="kaio", is_teacher=False)
        self.student5 = user_factory(name="felipe", is_teacher=False)
        self.student6 = user_factory(name="emily", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student1, self.student2, self.student3, self.student4, self.student5, self.student6],
            monitors=[self.monitor, self.teacher_monitor]
        )
        self.group1 = mommy.make(
            Group,
            discipline=self.discipline,
            title="Group test",
            students_limit=3,
            students=[self.student1, self.student2, self.student3]
        )
        self.group2 = mommy.make(
            Group,
            discipline=self.discipline,
            title="Group test",
            students_limit=3,
            students=[self.student4, self.student5]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            peer_review_available=True,
            peer_review_weight=1,
            is_closed=False
        )
        self.redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'peer_review:list',
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
        Group.objects.all().delete()

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

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/peer_review.html')
        self.assertTemplateUsed(response, 'peer_review/info.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.get(self.url)
        self.assertTrue('date' in response.context)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('discipline' in response.context)
        self.assertTrue('session' in response.context)
        self.assertTrue('group' in response.context)
        self.assertTrue('students' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('answer_form' in response.context)

    def test_teacher_can_see_the_peer_review(self):
        """
        Teacher can see the empty peer review list
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['students'], [])

    def test_teacher_monitor_can_see_the_peer_review(self):
        """
        Monitor teacher can see the empty peer review list
        """

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['students'], [])

    def test_monitor_can_see_the_peer_review(self):
        """
        Monitor can see the empty peer review list
        """

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['students'], [])

    def test_student_without_group_can_see_the_peer_review(self):
        """
        Student without group can see the empty peer review list
        """

        self.client.login(username=self.student6.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['students'], [])

    def test_user_can_not_see_the_peer_review(self):
        """
        Monitor can see the empty peer review list
        """

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path, status_code=302, target_status_code=302)

    def test_group_student1_can_see_the_peer_review(self):
        """
        Students within the group will be able to evaluate the members of their group at peer review
        """

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student1 in self.group1.students.all())
        self.assertTrue(self.student2 in response.context['students'])
        # self.assertTrue(self.student3 in response.context['students'])
        self.assertTrue(self.student4 not in response.context['students'])
        self.assertTrue(self.student5 not in response.context['students'])
        self.assertEqual(len(response.context['students']), 1)

    def test_group_student2_can_see_the_peer_review(self):
        """
        Students within the group will be able to evaluate the members of their group at peer review
        """

        self.client.login(username=self.student2.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student2 in self.group1.students.all())
        self.assertTrue(self.student1 in response.context['students'])
        # self.assertTrue(self.student3 in response.context['students'])
        self.assertTrue(self.student4 not in response.context['students'])
        self.assertTrue(self.student5 not in response.context['students'])
        self.assertEqual(len(response.context['students']), 1)

    def test_group_student3_can_see_the_peer_review(self):
        """
        Students within the group will be able to evaluate the members of their group at peer review
        """

        self.client.login(username=self.student3.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student3 in self.group1.students.all())
        self.assertTrue(self.student1 in response.context['students'])
        # self.assertTrue(self.student2 in response.context['students'])
        self.assertTrue(self.student4 not in response.context['students'])
        self.assertTrue(self.student5 not in response.context['students'])
        self.assertEqual(len(response.context['students']), 1)

    def test_group_student4_can_see_the_peer_review(self):
        """
        Students within the group will be able to evaluate the members of their group at peer review
        """

        self.client.login(username=self.student4.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student4 in self.group2.students.all())
        self.assertTrue(self.student1 not in response.context['students'])
        self.assertTrue(self.student2 not in response.context['students'])
        self.assertTrue(self.student3 not in response.context['students'])
        self.assertTrue(self.student5 in response.context['students'])
        self.assertEqual(len(response.context['students']), 1)

    def test_group_student5_can_see_the_peer_review(self):
        """
        Students within the group will be able to evaluate the members of their group at peer review
        """

        self.client.login(username=self.student5.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student5 in self.group2.students.all())
        self.assertTrue(self.student1 not in response.context['students'])
        self.assertTrue(self.student2 not in response.context['students'])
        self.assertTrue(self.student3 not in response.context['students'])
        self.assertTrue(self.student4 in response.context['students'])
        self.assertEqual(len(response.context['students']), 1)

    def test_teacher_can_see_peer_review_closed(self):
        """
        Only teacher can see the peer_review closed.
        """

        self.module.peer_review_available = False
        self.module.save()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['students'], [])

    def test_teacher_monitor_can_not_see_peer_review_closed(self):
        """
        Only teacher monitor can not see the peer_review closed.
        """

        self.module.peer_review_available = False
        self.module.save()
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path, status_code=302)

    def test_monitor_can_not_see_peer_review_closed(self):
        """
        Only monitor can not see the peer_review closed.
        """

        self.module.peer_review_available = False
        self.module.save()
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path, status_code=302)

    def test_student_can_not_see_peer_review_closed(self):
        """
        Only monitor can not see the peer_review closed.
        """

        self.module.peer_review_available = False
        self.module.save()
        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path, status_code=302)
