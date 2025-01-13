from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    photo = models.URLField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    provider = models.CharField(max_length=50, blank=True, null=True)  # e.g., "google", "facebook"

    def __str__(self):
        return self.username