from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200, blank=True
    )  # SEO 친화적인 URL을 만들기 위한 라벨
    url = models.URLField()  # 이미지의 원래 URL
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="images_liked", blank=True
    )

    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        제목 필드의 값을 기반으로 slug 필드를 자동으로 생성하도록 한다.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "images:detail",
            args=[self.id, self.slug],
        )
