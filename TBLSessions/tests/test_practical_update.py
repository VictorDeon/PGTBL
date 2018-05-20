from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession

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
        self.teacher = User.objects.create_user(
            username='someTeacher',
            email='teacherEmail@email.com',
            password='somepass'
            is_teacher=True
        )

        self.discipline = mommy.make('Discipline')
        self.discipline.teacher.add(self.teacher)

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=30
        )
        self.tbl_session = self.tbl_sessions[0]

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()

    def test_only_teacher_can_update(self):
        """
        Teacher and monitors that is a teacher can update the practical test.
        """
        self.teacher.login(
            username=self.teacher.username,
            password='somepass'
        )

        url = '/practical-test/edit/'

        successful_response = self.teacher.get(url, follow=True)

        self.assertEqual(successful_response.status_code, 200)
