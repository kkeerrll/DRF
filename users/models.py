from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    """
        Класс перечисления для определения ролей пользователя.

        Attributes:
            MEMBER (str): Значение роли 'member'.
            MODERATOR (str): Значение роли 'moderator'.
    """
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=35, null=True, blank=True, verbose_name='Телефон')
    country = models.CharField(max_length=35, null=True, blank=True, verbose_name='Страна')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
