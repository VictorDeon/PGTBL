"""
File to provides some global functionality for testing.
"""
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.six import BytesIO
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


def check_messages(self, response, tag, content):
    """
    Get the messages from django.contrib.messages
    Need to pass follow=True in the get or post method.
    """

    message = list(response.context.get('messages'))[0]
    self.assertEqual(message.tags, tag)
    self.assertEqual(message.message, _(content))


def list_transform(queryset):
    """
    Transform the queryset in a list to compare.
    """

    query_list = []

    for item in queryset:
        query_list.append(item)

    return query_list


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    if storage is None, the BytesIO containing the image data will be passed instead
    """

    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data

    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


def user_factory(qtd=1,
                 name='Test',
                 username='Test',
                 email='test',
                 password='test1234',
                 is_teacher=True,
                 **fields):
    """
    Create N users and return a list.
    """

    users = []
    count = User.objects.count()

    for n in range(qtd):
        user = User.objects.create_user(
            name='{0}{1}'.format(name, n+count),
            username='{0}{1}'.format(username, n+count),
            email='{0}{1}@gmail.com'.format(email, n+count),
            password=password,
            is_teacher=is_teacher,
            **fields
        )

        users.append(user)

    if qtd > 1:
        return users
    else:
        return user
