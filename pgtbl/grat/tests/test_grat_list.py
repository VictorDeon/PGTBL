from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from model_mommy import mommy

from core.test_utils import user_factory
from disciplines.models import Discipline
from modules.models import TBLSession
from questions.models import Question, Alternative

from datetime import timedelta

User = get_user_model()


class ListGRATTestCase(TestCase):
    """
    Test to list question into GRAT test.
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
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            irat_datetime=timezone.now() - timedelta(minutes=31),
            grat_datetime=timezone.now(),
            is_closed=False
        )
        self.questions = mommy.make(
            Question,
            title="Question",
            topic="Topic",
            level='Basic',
            is_exercise=False,
            session=self.module,
            _quantity=3
        )
        self.alternatives1 = mommy.make(
            Alternative,
            title="Alternative",
            question=self.questions[0],
            _quantity=4
        )
        self.alternatives2 = mommy.make(
            Alternative,
            title="Alternative",
            question=self.questions[1],
            _quantity=4
        )
        self.alternatives3 = mommy.make(
            Alternative,
            title="Alternative",
            question=self.questions[2],
            _quantity=4
        )
        self.alternatives1[0].is_correct = True
        self.alternatives1[0].save()
        self.alternatives2[1].is_correct = True
        self.alternatives2[1].save()
        self.alternatives3[0].is_correct = True
        self.alternatives3[0].save()
        self.now = timezone.localtime(timezone.now())
        self.redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'grat:list',
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
        Question.objects.all().delete()
        Alternative.objects.all().delete()

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

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grat/grat.html')
        self.assertTemplateUsed(response, 'grat/info.html')
        self.assertTemplateUsed(response, 'grat/date.html')
        self.assertTemplateUsed(response, 'grat/update.html')
        self.assertTemplateUsed(response, 'grat/progress_bar.html')
        self.assertTemplateUsed(response, 'grat/pagination.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertTrue('date' in response.context)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('irat_datetime' in response.context)
        self.assertTrue('grat_datetime' in response.context)
        self.assertTrue('discipline' in response.context)
        self.assertTrue('session' in response.context)
        self.assertTrue('questions' in response.context)
        self.assertTrue('date_form' in response.context)
        self.assertTrue('grat_form' in response.context)
        self.assertTrue('form1' in response.context)
        self.assertTrue('form2' in response.context)
        self.assertTrue('form3' in response.context)
        self.assertTrue('form4' in response.context)

    def test_grat_pagination(self):
        """
        Test to show question by pagination.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        paginator = response.context['paginator']
        self.assertEqual(paginator.count, 3)
        self.assertEqual(paginator.per_page, 1)
        self.assertEqual(paginator.num_pages, 3)

    def test_page_not_found(self):
        """
        Test to verify one page that not exists.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get('{0}?page=4'.format(self.url))
        self.assertEqual(response.status_code, 404)

    def test_teacher_can_see_the_grat_list(self):
        """
        Teacher can see the gRAT list
        with exercises questions.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_the_closed_session_grat_list(self):
        """
        Teacher can see the gRAT list when session is closed
        with exercises questions.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_grat_before_started(self):
        """
        Teacher can see the test before datetime stipulated.
        """

        # Now = 10:00, gRAt = 10:01, gRAT finish = 10:31
        self.module.grat_datetime = self.now + timedelta(minutes=1)
        self.module.save()

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_grat_started(self):
        """
        Teacher can see the test in the datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:50, gRAT finish = 10:20
        self.module.grat_datetime = self.now - timedelta(minutes=10)
        self.module.save()

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_grat_after_finished(self):
        """
        Teacher can see the test after datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:25, gRAt finish = 9:55
        self.module.grat_datetime = self.now - timedelta(minutes=self.module.grat_duration + 1)
        self.module.save()

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_monitor_can_see_the_grat_list(self):
        """
        Teacher monitor can see the gRAT list
        with exercises questions.
        """

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_monitor_can_see_the_closed_session_grat(self):
        """
        Teacher monitor can see the gRAT list when session is closed
        with exercises questions.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_monitor_can_see_grat_before_started(self):
        """
        Teacher monitor can see the test before datetime stipulated.
        """

        # Now = 10:00, gRAt = 10:01, gRAT finish = 10:31
        self.module.grat_datetime = self.now + timedelta(minutes=1)
        self.module.save()

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_monitor_can_see_grat_started(self):
        """
        Teacher monitor can see the test in the datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:50, gRAT finish = 10:20
        self.module.grat_datetime = self.now - timedelta(minutes=10)
        self.module.save()

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teacher_monitor_can_see_grat_after_finished(self):
        """
        Teacher monitor can see the test after datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:25, gRAt finish = 9:55
        self.module.grat_datetime = self.now - timedelta(minutes=self.module.grat_duration + 1)
        self.module.save()

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monitor_can_not_see_the_grat_list(self):
        """
        Monitor can not see the gRAT list
        with exercises questions.
        """

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_monitor_can_not_see_the_closed_session_grat(self):
        """
        Monitor can not see the gRAT list when session is closed
        with exercises questions.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_monitor_can_not_see_grat_before_started(self):
        """
        Monitor can not see the test before datetime stipulated.
        """

        # Now = 10:00, gRAt = 10:01, gRAT finish = 10:31
        self.module.grat_datetime = self.now + timedelta(minutes=1)
        self.module.save()

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_monitor_can_not_see_grat_started(self):
        """
        Monitor can not see the test in the datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:50, gRAT finish = 10:20
        self.module.grat_datetime = self.now - timedelta(minutes=10)
        self.module.save()

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_monitor_can_not_see_grat_after_finished(self):
        """
        Monitor can not see the test after datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:25, gRAt finish = 9:55
        self.module.grat_datetime = self.now - timedelta(minutes=self.module.grat_duration + 1)
        self.module.save()

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_student_can_see_the_grat_list(self):
        """
        Student can see the gRAT list
        with exercises questions.
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_can_not_see_the_closed_session_grat(self):
        """
        Student can not see the gRAT list when session is closed
        with exercises questions.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_student_can_not_see_grat_before_started(self):
        """
        Student can not see the test before datetime stipulated.
        """

        # Now = 10:00, gRAt = 10:01, gRAT finish = 10:31
        self.module.grat_datetime = self.now + timedelta(minutes=1)
        self.module.save()

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_student_can_see_grat_started(self):
        """
        Student can see the test in the datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:50, gRAT finish = 10:20
        self.module.grat_datetime = self.now - timedelta(minutes=10)
        self.module.save()

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_can_not_see_grat_after_finished(self):
        """
        Monitor can not see the test after datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:25, gRAt finish = 9:55
        self.module.grat_datetime = self.now - timedelta(minutes=self.module.grat_duration + 1)
        self.module.save()

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_path)

    def test_user_can_not_see_the_grat_list(self):
        """
        User that is not into discipline can not see the gRAT list
        with exercises questions.
        """

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_not_see_the_closed_session_grat(self):
        """
        User that is not into discipline can not see the gRAT list when session is closed
        with exercises questions.
        """

        self.module.is_closed = True
        self.module.save()
        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_not_see_grat_before_started(self):
        """
        User that is not into discipline can not see the test before datetime stipulated.
        """

        # Now = 10:00, gRAt = 10:01, gRAT finish = 10:31
        self.module.grat_datetime = self.now + timedelta(minutes=1)
        self.module.save()

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_not_see_grat_started(self):
        """
        User that is not into discipline can not see the test in the datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:50, gRAT finish = 10:20
        self.module.grat_datetime = self.now - timedelta(minutes=10)
        self.module.save()

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_not_see_grat_after_finished(self):
        """
        User that is not into discipline can not see the test after datetime stipulated.
        """

        # Now = 10:00, gRAT = 9:25, gRAt finish = 9:55
        self.module.grat_datetime = self.now - timedelta(minutes=self.module.grat_duration + 1)
        self.module.save()

        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)