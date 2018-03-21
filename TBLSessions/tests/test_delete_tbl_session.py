from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import File

User = get_user_model()


class DeleteTBLSessionTestCase(TestCase):
    """
    Test to delete a new tbl session.
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
        User can not delete a tbl session without logged in.
        """

        pass

    def test_delete_tbl_session_by_teacher(self):
        """
        Test to delete a tbl session by teacher.
        """

        pass

    def test_delete_tbl_session_by_monitors(self):
        """
        Test to delete a tbl session by monitors if they are a teacher.
        """

        pass

    def test_delete_tbl_session_by_student_fail(self):
        """
        Student can not delete a tbl session.
        """

        pass

    def test_delete_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not delete a tbl session.
        """

        pass
