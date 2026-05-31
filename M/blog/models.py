from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Blog(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='blogs/')
    author = models.CharField(max_length=100, default='مدیر')
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:blog-detail", args=[self.slug])

    class Meta:
        verbose_name = 'وبلاگ'
        verbose_name_plural = 'وبلاگ ها'

    def __str__(self):
        return self.title
