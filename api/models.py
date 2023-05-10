from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.validators import (RegexValidator)

message = ('Username содержит недопустимые символы {value}')


class UsernameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(
            RegexValidator(r'^[\w.@+-]+$', message)
        )


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True, max_length=settings.EMAIL
    )
    username = UsernameField(
        verbose_name='Имя пользователя',
        help_text='Только буквы, цифры, @, +, -, _',
        max_length=settings.USERNAME,
        null=True,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max((len(role[1]) for role in ROLES)),
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_is_not_me'
            )
        ]

    def __str__(self):
        return f'{self.username}({self.email})'
