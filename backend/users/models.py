from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=50
    )
    first_name = models.CharField(
        'Имя',
        max_length=50
    )
    second_name = models.CharField(
        'Фамилия',
        max_length=50
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        max_length=124
    )

    class Meta:
        ordering = ('username',)

    
    def __str__(self):
        return self.username
