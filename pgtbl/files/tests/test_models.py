from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from model_mommy import mommy

from core.test_utils import user_factory
from disciplines.models import Discipline
from files.models import DisciplineFile

User = get_user_model()


class FileTestCase(TestCase):
    """
    Test to validate file fields.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.teacher = user_factory(name="maria", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345"
        )
        text_file = SimpleUploadedFile("text.txt", b'This is some text file')
        self.file = mommy.make(
            DisciplineFile,
            title='File title',
            description='File Description',
            extension='txt',
            archive=text_file,
            discipline=self.discipline
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.file.delete()

    def test_get_title_method(self):
        """
        Test title attribute from file model
        """

        self.assertEqual(self.file.get_title(), "file_title")

