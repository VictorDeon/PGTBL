from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession
from peer_review.models import PeerReviewSubmission

User = get_user_model()


class AnswerPeerReviewTestCase(TestCase):
    """
    Test to answer Peer Review
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.teacher_monitor = user_factory(name="otavio", is_teacher=True)
        self.student = user_factory(name="joana", is_teacher=False)
        self.student1 = user_factory(name="joao", is_teacher=False)
        self.student2 = user_factory(name="victor", is_teacher=False)
        self.student3 = user_factory(name="kaio", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student, self.student1, self.student2, self.student3],
            monitors=[self.monitor, self.teacher_monitor]
        )
        self.group1 = mommy.make(
            Group,
            discipline=self.discipline,
            title="Group test",
            students_limit=3,
            students=[self.student1, self.student2]
        )
        self.group2 = mommy.make(
            Group,
            discipline=self.discipline,
            title="Group test",
            students_limit=3,
            students=[self.student3]
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
            'peer_review:answer-review',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk,
                'student_id': self.student2.pk,
                'peer_review_page': 1
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

    def test_correct_answer_ok(self):
        """
        Insert a score to group member
        """

        data = {
            'score': 70,
            'comment': "Ola fulano"
        }

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 1)
        self.assertEqual(70, PeerReviewSubmission.objects.first().score)
        self.assertEqual("Ola fulano", PeerReviewSubmission.objects.first().comment)
        check_messages(
            self, response,
            tag='alert-success',
            content="Peer Review answered successfully."
        )

    def test_negative_score_answer(self):
        """
        Insert negative score to group member
        """

        data = {
            'score': -5,
            'comment': "Ola fulano"
        }

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You can't insert a score bigger than 100 or less than 0"
        )

    def test_score_bigger_than_100_answer(self):
        """
        Insert score bigger than 100 to group member
        """

        data = {
            'score': 101,
            'comment': "Ola fulano"
        }

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You can't insert a score bigger than 100 or less than 0"
        )

    def test_empty_comment_answer(self):
        """
        Insert a score without comment to group member
        """

        data = {
            'score': 88,
            'comment': ""
        }

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 1)
        check_messages(
            self, response,
            tag='alert-success',
            content="Peer Review answered successfully."
        )

    def test_submit_to_member_out_group(self):
        """
        submit a peer review to a member out of group.
        """

        data = {
            'score': 88,
            'comment': "Ola fulano"
        }

        url = reverse_lazy(
            'peer_review:answer-review',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk,
                'student_id': self.student3.pk,
                'peer_review_page': 1
            }
        )

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_submit_twice(self):
        """
        Student can not submit a peer review twice to the same student
        """

        data = {
            'score': 88,
            'comment': "Ola fulano"
        }

        self.client.login(username=self.student1.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 1)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(PeerReviewSubmission.objects.count(), 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You already submit a review to this student."
        )

    def test_student_need_to_be_inside_group_to_submit(self):
        """
        Student need to be inside a group to submit a peer review.
        """

        data = {
            'score': 88,
            'comment': "Ola fulano"
        }

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, self.redirect_path)
        self.assertEqual(PeerReviewSubmission.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )