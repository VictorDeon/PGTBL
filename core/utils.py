# Django functions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
# Python functions
import hashlib
import string
import random


# --------------------------- RESET PASSWORD KEY -------------------------- #


def random_key(size=5):
    """
    Generates the key with a random character set.
    """

    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def generate_hash_key(salt, random_str_size=5):
    """
    Function to generate the hash key from the salt which is some user
    information.
    """

    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


# ---------------------------- PERMISSIONS -------------------------------- #


def create_permission(codename, name, model):
    """
    Create a new permission.
    Ex:
        create_permission(
            codename='can_create_discipline_' + str(obj.id),
            name='Can edit instance with id ' + str(obj.id),
            model=Discipline
        )
    """

    content_type = ContentType.objects.get_for_model(model)

    return Permission.objects.create(
        codename=codename,
        name=name,
        content_type=content_type
    )


def insert_group_permissions(group, permissions_codename):
    """
    Insert permissions in group.
    """

    for codename in permissions_codename:
        permission = get_object_or_404(Permission, codename=codename)
        group.permissions.add(permission)


def insert_user_permissions(user, permissions_codename):
    """
    Insert permissions in user.
    """

    for codename in permissions_codename:
        permission = get_object_or_404(Permission, codename=codename)
        user.user_permissions.add(permission)
