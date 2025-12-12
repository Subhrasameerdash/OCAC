from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


User = get_user_model()


class Post(models.Model):
	"""Single blog post authored by a registered user."""

	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	content = models.TextField()
	hero_image = models.ImageField(upload_to='posts/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['slug']), models.Index(fields=['created_at'])]

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.title)
			slug = base_slug
			suffix = 1
			while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
				slug = f"{base_slug}-{suffix}"
				suffix += 1
			self.slug = slug
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'slug': self.slug})
