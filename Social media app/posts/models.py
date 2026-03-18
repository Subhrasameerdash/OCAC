from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    A post can be either a *media* post (image/video + caption)
    or a *thought* post (text-only, styled as a card).
    """
    POST_TYPES = [
        ('media', 'Media'),
        ('thought', 'Thought'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='thought')
    caption = models.TextField(max_length=2200, blank=True, default='')
    media = models.FileField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # ── Fat-model helpers ─────────────────────────────────────────────
    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if user.is_anonymous:
            return False
        return self.likes.filter(user=user).exists()

    def is_video(self):
        if self.media:
            return self.media.name.lower().endswith(('.mp4', '.webm', '.mov', '.avi'))
        return False

    def __str__(self):
        return f'{self.author.username} — {self.post_type} ({self.pk})'


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} ♥ post {self.post.pk}'


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}: {self.text[:40]}'
