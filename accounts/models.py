from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
