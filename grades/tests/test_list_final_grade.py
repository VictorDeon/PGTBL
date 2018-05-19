from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from grades.models import Grade, FinalGrade

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
        self.discipline = mommy.make('Discipline')
        self.student = User.objects.create_user(
            username='student',
            email='stu@gmail.com',
            password='senha123',
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

        pass
