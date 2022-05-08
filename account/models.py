from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    JOBS = (
        (1, 'Teacher'),
        (2, 'Student'),
        (3, 'Other')
    )

    photo = models.ImageField(upload_to='user/')
    job = models.SmallIntegerField(choices=JOBS, default=3)
    confirmed = models.BooleanField(default=False)
