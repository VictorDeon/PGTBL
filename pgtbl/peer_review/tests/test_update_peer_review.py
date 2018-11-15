from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from grades.models import Grade
from groups.models import Group
from modules.models import TBLSession
from peer_review.models import PeerReviewSubmission

User = get_user_model()


class UpdatePeerReviewTestCase(TestCase):
    """
    Test to update Peer Review
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.teacher_monitor = user_factory(name="otavio", is_teacher=True)
        self.student1 = user_factory(name="joana", is_teacher=False)
        self.student2 = user_factory(name="carol", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student1, self.student2],
            monitors=[self.monitor, self.teacher_monitor]
        )
        self.group = mommy.make(
            Group,
            discipline=self.discipline,
            title="Group test",
            students_limit=3,
            students=[self.student1, self.student2]
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
        self.success_redirect = reverse_lazy(
            'peer_review:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'peer_review:update',
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

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_not_update_peer_review_by_monitor_teacher(self):
        """
        Monitor teacher can not update a peer review
        """

        data = {'peer_review_available': True, 'peer_review_weight': 3}
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_path)
        self.module.refresh_from_db()
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_not_update_peer_review_by_monitor(self):
        """
        Monitor can not update a peer review
        """

        data = {'peer_review_available': True, 'peer_review_weight': 3}
        self.client.login(username=self.monitor.username, password='test1234')
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_path)
        self.module.refresh_from_db()
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_not_update_peer_review_by_student(self):
        """
        Student can not update a peer review
        """

        data = {'peer_review_available': True, 'peer_review_weight': 3}
        self.client.login(username=self.student1.username, password='test1234')
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_path)
        self.module.refresh_from_db()
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_not_update_peer_review_by_user(self):
        """
        User outside discipline can not update a peer review
        """

        data = {'peer_review_available': True, 'peer_review_weight': 3}
        self.client.login(username=self.user.username, password='test1234')
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        response = self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_update_peer_review_by_teacher(self):
        """
        Update peer review weight by teacher
        """

        data = {'peer_review_available': True, 'peer_review_weight': 3}
        self.client.login(username=self.teacher.username, password='test1234')
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 1)
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.success_redirect)
        self.module.refresh_from_db()
        self.assertEqual(self.module.peer_review_available, True)
        self.assertEqual(self.module.peer_review_weight, 3)
        check_messages(
            self, response,
            tag='alert-success',
            content="Pair Review updated successfully."
        )

    # def test_close_peer_review_by_teacher(self):
    #     """
    #     Close peer review by teacher and calculate/create a students grade
    #     """
    #
    #     PeerReviewSubmission.objects.create(
    #         session=self.module,
    #         score=70,
    #         comment="Ola fulano",
    #         user=self.student1,
    #         student=self.student2,
    #         group=self.group
    #     )
    #     grade1 = Grade.objects.create(
    #         session=self.module,
    #         student=self.student1,
    #         group=self.group,
    #         irat=7,
    #         grat=10,
    #         practical=8,
    #         peer_review=8
    #     )
    #
    #     data = {'peer_review_available': False, 'peer_review_weight': 1}
    #     self.client.login(username=self.teacher.username, password='test1234')
    #     self.assertEqual(self.module.peer_review_available, True)
    #     self.assertEqual(self.module.peer_review_weight, 1)
    #     self.assertEqual(PeerReviewSubmission.objects.count(), 1)
    #     self.assertEqual(Grade.objects.count(), 1)
    #     response = self.client.post(self.url, data, follow=True)
    #     self.assertRedirects(response, self.success_redirect)
    #     self.module.refresh_from_db()
    #     self.assertEqual(self.module.peer_review_available, False)
    #     self.assertEqual(self.module.peer_review_weight, 1)
    #     self.assertEqual(Grade.objects.count(), 2)
    #     check_messages(
    #         self, response,
    #         tag='alert-success',
    #         content="Pair Review updated successfully."
    #     )
    #      self.assertEqual(grade1.peer_review, 8.0)
    #      grade2 = Grade.objects.get(student=self.student2)
    #      self.assertEqual(grade2.peer_review, 7.0)
