from typing import Any, Iterable
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils.text import slugify

class PublishedPostManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()
        qs = qs.filter(status=Post.Status.PUBLISHED)
        return qs

    def create(self, **kwargs: Any) -> Any:
        kwargs.setdefault("status", Post.Status.PUBLISHED)
        return super().create(**kwargs)
    

class Category(models.Model):
    name = models.CharField(max_length=50)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "D", "초안"
        PUBLISHED = "P", "발행"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT
    )
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedPostManager()

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.slugify()
        return super().save(force_insert, force_update, using, update_fields)

    def slugify(self, force=False):
        if force or not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            slug_max_length = self._meta.get_field("slug").max_length
            self.slug = self.slug[:slug_max_length]
            self.slug += "-" + uuid4().hex[:8]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="unique_slug")
        ]



