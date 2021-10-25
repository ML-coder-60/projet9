# authentication/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMINISTRATOR = 'ADMINISTRATOR'
    USER = 'USER'

    ROLE_CHOICES = (
        (ADMINISTRATOR, 'Administrateur'),
        (USER, 'Utilisateur'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    email = models.EmailField()
    EMAIL_FIELD = 'email'

