from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession

User = get_user_model()


class UpdatePracticalTestCase(TestCase):
    """
    Test to update the practical test.
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
        self.session = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="TBL session title",
            description="TBL session description"
        )
        self.url = reverse_lazy(
            'practical:update',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.pk
            }
        )
        self.data = {
            'title': "TBL session title",
            'description': "TBL session description",
            'practical_weight': 2
        }

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.session.delete()

    def test_redirect_to_login(self):
        """
        User can not see practical test details without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_monitor_teacher_can_update_practical_test(self):
        """
        Teacher and monitors that is a teacher can update the practical test,
        before it being opened.
        """

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        self.assertEqual(self.session.practical_weight, 4)
        response = self.client.post(self.url, self.data, follow=True)
        practical_url = reverse_lazy(
            'practical:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.pk
            }
        )
        self.assertRedirects(response, practical_url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.practical_weight, self.data['practical_weight'])
        check_messages(
            self, response,
            tag='alert-success',
            content='Practical test updated successfully.'
        )

    def test_teacher_can_update_practical_test(self):
        """
        Teacher can update the practical test, before it being opened.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        self.assertEqual(self.session.practical_weight, 4)
        response = self.client.post(self.url, self.data, follow=True)
        practical_url = reverse_lazy(
            'practical:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.pk
            }
        )
        self.assertRedirects(response, practical_url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.practical_weight, self.data['practical_weight'])
        check_messages(
            self, response,
            tag='alert-success',
            content='Practical test updated successfully.'
        )

    def test_student_can_not_update_practical_test(self):
        """
        Student can not update practical test
        """

        self.session.is_closed = False
        self.session.save()
        self.client.login(username=self.student.username, password='test1234')
        self.assertEqual(self.session.practical_weight, 4)
        response = self.client.post(self.url, self.data, follow=True)
        session_url = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.pk
            }
        )
        self.assertRedirects(response, session_url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.practical_weight, 4)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_monitor_can_not_update_practical_test(self):
        """
        Monitor that is not a teacher can't update practical test
        """

        self.client.login(username=self.monitor.username, password='test1234')
        self.assertEqual(self.session.practical_weight, 4)
        response = self.client.post(self.url, self.data, follow=True)
        session_url = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.pk
            }
        )
        self.assertRedirects(response, session_url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.practical_weight, 4)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
