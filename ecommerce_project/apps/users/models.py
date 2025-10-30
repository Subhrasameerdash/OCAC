from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Optional profile information extending Django's built-in user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} profile"
