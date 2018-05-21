from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from grades.models import Grade, FinalGrade
from TBLSessions.models import TBLSession
from disciplines.models import Discipline
from groups.models import User
from core.test_utils import (
    list_transform, check_messages, user_factory
)

User = get_user_model()


class ListFinalGradeTestCase(TestCase):
    """
    Test to list final grades.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.monitors = user_factory(qtd=3)
        self.student = User.objects.create_user(
        username='student',
        email='stu@gmail.com',
        password='senha123',
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline04',
            course='Engineering',
            password='12345',
            students_limit=10,
            monitors_limit=3,
            students=[self.student],
            monitors=self.monitors,
            make_m2m=True
        )
        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline = self.discipline,
            title = 'title',
            description = 'description',
            practical_description = 'description'
            )
        self.grade = mommy.make(
            Grade,
            session = self.tbl_sessions,
            student = self.student,
            irat=2.0,
            grat=2.0,
            practical=2.0
            )
        self.final_grade = mommy.make(
            FinalGrade,
            discipline = self.discipline,
            student = self.student
        )
        self.url = reverse_lazy('grades:result', kwargs={'slug': self.discipline.slug})
        self.login_redirect = '/login/?next=/profile/' + self.discipline.slug + '/grades/'


    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not see the final grade list without logged in.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect, status_code=302, target_status_code=200)

    def test_users_can_see_the_grades(self):
        """
        User like students, monitors and teacher can see the list of final
        grades.
        """

        pass

    def test_calcule_final_grade(self):
        """
        Unit test about calcule_final_grade() method from FinalGrade model.

        """
        assert self.final_grade.calcule_final_grade() == 2
