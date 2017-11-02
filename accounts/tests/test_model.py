from django.test import TestCase
from accounts.models import User


class ModelTestCase(TestCase):
    """
    Test all features about user model.
    TODO:
        - Test username validation.
        - Test email validation
        - Test fields validation
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.superuser = User.objects.create_superuser(
            name='Victor Arnaud',
            username='victorhad',
            email='victorhad@gmail.com',
            password='victorhad123456'
        )
        self.user1 = User.objects.create_user(
            name='Pedro',
            username='pedro',
            email='pedro@gmail.com',
            password='pedro123456'
        )
        self.user2 = User.objects.create_user(
            name='Maria de Fatima',
            username='maria',
            email='maria@gmail.com',
            password='maria123456'
        )
        self.user3 = User.objects.create_user(
            name='Jose da Silva Pereira',
            username='jose',
            email='jose@gmail.com',
            is_teacher=False,
            password='jose123456',
            institution='UnB',
            course='Software Engineering',
            photo='img/photo01.png'
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()

    def test_full_name(self):
        """
        Test to get the full name of user
        """

        self.assertEquals(self.superuser.get_full_name(), self.superuser.name)
        self.assertEquals(self.user1.get_full_name(), self.user1.name)
        self.assertEquals(self.user2.get_full_name(), self.user2.name)
        self.assertEquals(self.user3.get_full_name(), self.user3.name)

    def test_short_name(self):
        """
        Test to get the short name of user, the first name with the last name
        """

        self.assertEquals(self.superuser.get_short_name(), 'Victor Arnaud')
        self.assertEquals(self.user1.get_short_name(), self.user1.name)
        self.assertEquals(self.user2.get_short_name(), 'Maria Fatima')
        self.assertEquals(self.user3.get_short_name(), 'Jose Pereira')

    def test_is_teacher_or_students(self):
        """
        Teste to verify if user is a teacher or a student
        """

        self.assertEquals(self.superuser.is_teacher, True)
        self.assertEquals(self.user1.is_teacher, True)
        self.assertEquals(self.user2.is_teacher, True)
        self.assertEquals(self.user3.is_teacher, False)
