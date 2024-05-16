from typing import Any, Iterable
from uuid import uuid4
from django.conf import settings
from django.conf.locale import ckb
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.text import slugify

from core.model_fields import BooleanYNField, IPv4AddressIntegerField

class PublishedPostManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()
        qs = qs.filter(status=Post.Status.PUBLISHED)
        return qs

    def create(self, **kwargs: Any) -> Any:
        kwargs.setdefault("status", Post.Status.PUBLISHED)
        return super().create(**kwargs)
    

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(TimestampedModel):
    class Status(models.TextChoices):
        DRAFT = "D", "초안"
        PUBLISHED = "P", "발행"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="blog_post_set",
        related_query_name="blog_post",
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT
    )
    content = models.TextField()
    tag_set = models.ManyToManyField(
        "Tag", 
        blank=True,
        related_name="blog_post_set",
        related_query_name="blog_post",
        through="PostTagRelation",
        through_fields=("post", "tag")
    )

    objects = models.Manager()
    published = PublishedPostManager()

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self) -> None:
        self.slugify()
        return super().save()

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
        verbose_name = "포스팅"
        verbose_name_plural = "포스팅 목록"
        permissions = [
            ("view_premium_post", f"Can view premium {verbose_name}")
        ]


class Comment(TimestampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()


class AccessLog(TimestampedModel):
    ip_generic = models.GenericIPAddressField(protocol="IPv4")
    ip_int = IPv4AddressIntegerField()


class Article(TimestampedModel):
    title = models.CharField(max_length=100)
    is_public_ch = models.CharField(
        max_length=1,
        choices=[
            ("Y", "예"),
            ("N", "아니오")
        ],
        default="N"
    )
    is_public_yn = BooleanYNField(default=False)


class Review(TimestampedModel):
    message = models.TextField()
    rating = models.SmallIntegerField(
        # validators=[
        #     MinValueValidator(1),
        #     MaxValueValidator(5),
        # ]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1, rating__lte=5),
                name="blog_review_rating_gte_1_lte_5"
            )
        ]
        db_table_comment = "사용자 리뷰와 평점을 저장하는 테이블. 평점(rating)은 1에서 5 사이의 값으로 제한."


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name = "blog_tag_name_unique"
            )
        ]
        indexes = [
            models.Index(
                fields=["name"],
                name="blog_tag_name_like",
                opclasses=["varchar_pattern_ops"]
            )
        ]


class PostTagRelation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "tag"],
                name="blog_post_tag_relation_unique",
            )
        ]


class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=100)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "student", "course", Lower("semester"),      # 다수의 expression 지정
                # fields=["student", "course", "semester"],  # 단순 필드명 나열
                name="blog_enrollment_uniq"),
        ]