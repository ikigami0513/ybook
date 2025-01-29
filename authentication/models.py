import uuid, os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

def user_avatar_file_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return os.path.join(f"users/avatars/{instance.id}.{uuid.uuid4()}{file_extension}")

class User(AbstractUser):
    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to=user_avatar_file_path, null=True, blank=True)
    