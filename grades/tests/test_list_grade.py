from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from core.test_utils import check_messages
from model_mommy import mommy
from grades.models import Grade, FinalGrade
from TBLSessions.models import TBLSession
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from core.test_utils import user_factory

User = get_user_model()


class ListGradeTestCase(TestCase):
    """
    Test to list session grades.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.teacher = user_factory(name='Pedro')
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
            make_m2m=True
        )
        self.session = mommy.make(
            TBLSession,
            discipline = self.discipline,
            title = 'title',
            description = 'description',
            practical_description = 'description'
            )
        self.grade = mommy.make(
            Grade,
            session = self.session,
            student = self.student,
            irat=2.0,
            grat=2.0,
            practical=2.0
            )
        self.url = reverse_lazy('grades:list', kwargs={'slug': self.discipline.slug, 'pk':self.session.pk})
        self.login_redirect = '/login/?next=' + str(self.url)

    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not see the grade list without logged in.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect, status_code=302, target_status_code=200)

    def test_users_can_see_the_grades(self):
        """
        User like students, monitors and teacher can see the list of grades.
        """

        self.client.login(username=self.student.username,
                          password='senha123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        grades_seen = Grade.objects.filter(student=self.student,
                                           irat=2.0, grat=2.0, practical=2.0).count()
        self.assertTrue(grades_seen > 0)

    def test_calculate_session_grade(self):
        """
        Unit test about calculate_session_grade() method from Grade model.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat=2.0,
            grat=2.0,
            practical=2.0)

        session_grade = grade.calcule_session_grade()
        self.assertEqual(session_grade, 2.0)

    def test_calculate_session_grade_with_peer_review(self):
        """
        Unit test about calculate_session_grade()
        when peer review is available.
        """

        session = TBLSession(peer_review_available=True)
        grade = Grade(
            session=session,
            irat=2.0,
            grat=2.0,
            practical=2.0,
            peer_review=4.0)

        session_grade = grade.calcule_session_grade()
        self.assertEqual(session_grade, 2.2)

    def test_calculate_session_grade_with_irat_string_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with iRAT receiving a string value.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat='abc',
            grat=2.0,
            practical=2.0)

        with self.assertRaises(TypeError):
            grade.calcule_session_grade()

    def test_calculate_session_grade_with_grat_string_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with gRAT receiving a string value.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat=2.0,
            grat='def',
            practical=2.0)

        with self.assertRaises(TypeError):
            grade.calcule_session_grade()

    def test_calculate_session_grade_with_pratical_string_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with pratical receiving a string value.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat=2.0,
            grat=2.0,
            practical='fgh')

        with self.assertRaises(TypeError):
            grade.calcule_session_grade()

    def test_calculate_session_grade_with_peer_review_string_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with peer review receiving a string value.
        """

        session = TBLSession(peer_review_available=True)
        grade = Grade(
            session=session,
            irat=2.0,
            grat=2.0,
            practical=2.0,
            peer_review='ijk')

        with self.assertRaises(TypeError):
            grade.calcule_session_grade()

    def test_calculate_session_grade_with_irat_negative_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with a nagative irat.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat=-10,
            grat=2.0,
            practical=2.0)

        with self.assertRaises(ValidationError):
            session_grade = grade.session.full_clean()

    def test_calculate_session_grade_with_grat_negative_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with a nagative grat.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat=1.0,
            grat=-2.0,
            practical=2.0)

        with self.assertRaises(ValidationError):
            session_grade = grade.session.full_clean()

    def test_calculate_session_grade_with_pratical_negative_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with a nagative pratical.
        """

        session = TBLSession()
        grade = Grade(
            session=session,
            irat=1.0,
            grat=2.0,
            practical=-2.0)

        with self.assertRaises(ValidationError):
            session_grade = grade.session.full_clean()

    def test_calculate_session_grade_with_peer_review_negative_value(self):
        """
        Unit test about calculate_session_grade() method from Grade model with peer review receiving a negative value.
        """

        session = TBLSession(peer_review_available=True)
        grade = Grade(
            session=session,
            irat=2.0,
            grat=2.0,
            practical=2.0,
            peer_review=-1.3)

        with self.assertRaises(ValidationError):
            session_grade = grade.session.full_clean()
