from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from modules.models import TBLSession

User = get_user_model()


class TBLSessionUpdateTestCase(TestCase):
    """
    Test to update a TBL session.
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
        User can not update a TBL session without logged in.
        """

        pass

    def test_update_tbl_session_by_teacher(self):
        """
        Test to update a tbl session by teacher.
        """

        pass

    def test_update_tbl_session_by_monitors(self):
        """
        Test to update a tbl session by monitors if monitor is a teacher.
        """

        pass

    def test_update_tbl_session_fail(self):
        """
        User can not update a tbl session with invalid fields.
        """

        pass

    def test_update_tbl_session_by_student_fail(self):
        """
        Student can not update a tbl session.
        """

        pass

    def test_update_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not update a tbl session.
        """

        pass
