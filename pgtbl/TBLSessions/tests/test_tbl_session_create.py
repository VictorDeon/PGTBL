from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession

User = get_user_model()


class TBLSessionCreateTestCase(TestCase):
    """
    Test to create a new TBL session.
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
        User can not create a new TBL session without logged in.
        """

        pass

    def test_create_tbl_session_by_teacher(self):
        """
        Test to create a new tbl session by teacher.
        """

        pass

    def test_create_tbl_session_by_monitors(self):
        """
        Test to create a new tbl session by monitors if monitor is a teacher.
        """

        pass

    def test_create_tbl_session_fail(self):
        """
        User can not create a tbl session with invalid fields.
        """

        pass

    def test_create_tbl_session_by_student_fail(self):
        """
        Student can not create a tbl session.
        """

        pass

    def test_create_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not create a tbl session.
        """

        pass
