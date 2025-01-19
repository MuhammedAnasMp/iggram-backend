from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    photo = models.URLField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class UserProvider(models.Model):
    user = models.ForeignKey(UserProfile, related_name="providers", on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=50)  # e.g., "google", "facebook"
    provider_email = models.EmailField(max_length=254, blank=True, null=True)  # Email associated with the provider

    def __str__(self):
        return f"{self.user.username}  {self.provider_name} ({self.provider_email})"