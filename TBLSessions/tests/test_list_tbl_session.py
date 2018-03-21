from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import File

User = get_user_model()


class ListTBLSessionTestCase(TestCase):
    """
    Test to list tbl sessions.
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
        User can not see the tbl session list without logged in.
        """

        pass

    def test_tbl_session_pagination(self):
        """
        Test to show tbl session by pagination.
        """

        pass

    def test_users_can_see_the_tbl_sessions(self):
        """
        User like students, monitors and teacher can see the list of tbl
        sessions.
        """

        pass
