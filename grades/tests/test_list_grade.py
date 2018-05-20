from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from grades.models import Grade, FinalGrade
from TBLSessions.models import TBLSession

User = get_user_model()


class ListGradeTestCase(TestCase):
    """
    Test to list session grades.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not see the grade list without logged in.
        """

        pass

    def test_users_can_see_the_grades(self):
        """
        User like students, monitors and teacher can see the list of grades.
        """

        pass

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
