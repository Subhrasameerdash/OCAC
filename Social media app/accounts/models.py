from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extended user model with profile fields and follow system.
    Login is possible via username OR email (see backends.py).
    """
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(max_length=300, blank=True, default='')
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default_avatar.png',
        blank=True,
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )

    # ── Fat-model helpers ─────────────────────────────────────────────
    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def is_following(self, user):
        """Return True if *this* user follows `user`."""
        return user.followers.filter(pk=self.pk).exists()

    def __str__(self):
        return self.username
