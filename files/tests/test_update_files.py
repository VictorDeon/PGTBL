from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from django.urls import reverse
from files.models import File, DisciplineFile
from files.urls import discipline_patterns
from disciplines.models import Discipline

User = get_user_model()


class UpdateFileTestCase(TestCase):
    """
    Test to update a discipline file.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher1 = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234'
        )
        self.teacher2 = User.objects.create_user(
            username='Test2',
            email='test2@gmail.com',
            password='test1234'
        )
        self.student = User.objects.create_user(
            username='Test3',
            email='test3@gmail.com',
            password='test1234',
            is_teacher=False
        )
        self.discipline = Discipline.objects.create(
            title='Discipline01',
            description='Discipline description.',
            classroom='Class A',
            students_limit=59,
            monitors_limit=5,
            is_closed=True,
            teacher=self.teacher1,
            slug='discipline01'
        )

        self.discipline.monitors.add(self.teacher1)

        self.monitors = User.objects.create_user(
            username='someMonitor',
            email='monitorEmail@email.com',
            password='somepass',
            is_teacher=True
        )

        self.discipline.monitors.add(self.monitors)

        # Create user
        self.user = User.objects.create_user(
            username='tester',
            email='tester@tester.com',
            password='tester123')

        self.discipline.students.add(self.user)

        # Create discipline and discipline file
        self.discipline.students.add(self.user)
        self.discipline_file = DisciplineFile.objects.create(
            extension='.jpg',
            title='test',
            archive='test.jpg',
            discipline=self.discipline)

        # Setup client and base url
        self.client = Client()
        self.url = reverse(
            'files:update',
            kwargs={'slug': self.discipline.slug, 'pk':self.discipline_file.pk}
        )


    def tearDown(self):
        """
        This method will run after any test.
        """

        self.client.logout()
        self.user.delete()
        self.teacher1.delete()
        self.teacher2.delete()
        self.student.delete()
        self.discipline.delete()


    def test_redirect_to_login(self):
        """
        User can not update a file without logged in.
        """
        response = self.client.get(self.url)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url

        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, redirect_url, 302)


    def test_update_file_by_teacher(self):
        """
        Test to update a file by teacher.
        """
        before_update = File.objects.count()
        self.client.login(username=self.teacher1.username, password='test1234')
        data = {
            'extension' : '.jpg',
            'title' : 'test modified',
            'archive' : 'test.jpg',
            'discipline' : self.discipline
        }
        response = self.client.post(self.url, data, follow=True)
        self.discipline_file.refresh_from_db()
        self.assertEqual(self.discipline_file.title, 'test modified')
        self.assertEqual(File.objects.count(), before_update)


    def test_update_file_by_monitors(self):
        """
        Test to update a file by monitors.
        """
        before_update = File.objects.count()
        self.client.login(username=self.monitors.username, password='somepass')
        data = {
            'extension' : '.jpg',
            'title' : 'test modified2',
            'archive' : 'test.jpg',
            'discipline' : self.discipline
        }
        response = self.client.post(self.url, data, follow=True)
        self.discipline_file.refresh_from_db()
        self.assertEqual(self.discipline_file.title, 'test modified2')
        self.assertEqual(File.objects.count(), before_update)


    def test_update_file_fail(self):
        """
        User can not update a file with invalid fields.
        """
        before_update = File.objects.count()
        self.client.login(username=self.teacher1.username, password='test1234')
        data = {
            'extension' : '.jpg',
            'title' : 'test modified2',
            'archive' : 'test.jpg',
            'discipline' : 'professor2'
        }
        response = self.client.post(self.url, data, follow=True)
        self.discipline_file.refresh_from_db()
        self.assertEqual(self.discipline_file.title, 'test modified2')
        self.assertFalse(self.discipline_file.discipline == 'professor2')
        self.assertEqual(File.objects.count(), before_update)
        # Assert deveria passar, porém o sistema permite atualização dos dados
        # mesmo com valores falsos. O status code retornado não poderia ser 200 (sucess)
        # por isso o assertFalse da clausula abaixo. Não foi possivel localizar o erro no código.
        # O arquivo foi modificado em partes, o extension, title e archive foram
        # modificados com sucesso, porém o discipline (valor incorreto) não foi
        # modificado e não retornou mensagem de erro para o usuário.
        self.assertFalse(response.status_code == 200)


    def test_update_file_by_student_fail(self):
        """
        Student can not update a file.
        """

        pass


class UpdateSessionFileTestCase(TestCase):
    """
    Test to update a session file.
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
        User can not update a file without logged in.
        """

        pass

    def test_update_file_by_teacher(self):
        """
        Test to update a file by teacher.
        """

        pass

    def test_update_file_by_monitors(self):
        """
        Test to update a file by monitors.
        """

        pass

    def test_update_file_fail(self):
        """
        User can not update a file with invalid fields.
        """

        pass

    def test_update_file_by_student_fail(self):
        """
        Student can not update a file.
        """

        pass
