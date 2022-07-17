from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{4}-?\d{4}$")],
    )
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.email
