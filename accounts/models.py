from typing import Iterable
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friend_set = models.ManyToManyField(
        to="self",
        blank=True,
        # to="self"에서 디폴트 True
        symmetrical=True,
        # related_name="friend_set",
        related_query_name="friend_user",
    )

    follower_set = models.ManyToManyField(
        to="self",
        blank=True,
        # to="self"에서 디폴트 True
        symmetrical=False,
        # symmetrical=False 에서는 related_name을 지원
        related_name="following_set",
        related_query_name="following",
    )


class SuperUserManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()
        return qs.filter(is_superuser=True)
    

class SuperUser(User):
    objects = SuperUserManager()

    class Meta:
        proxy = True

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.is_superuser = True
        return super().save(force_insert, force_update, using, update_fields)



class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    address = models.CharField(max_length=100, blank=True)
    point = models.PositiveIntegerField(default=0)