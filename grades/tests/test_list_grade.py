from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import File

User = get_user_model()


class ListGradeTestCase(TestCase):
    """
    Test to list session grades.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        pass

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

        pass
