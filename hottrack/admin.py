from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from .utils.melon import get_likes_dict

from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = ["name", "artist_name", "album_name"]
    list_display = [
        "cover_image_tag",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]
    list_filter = ["genre", "release_date"]
    actions = ["update_like_count"]

    def update_like_count(self, request: HttpRequest, queryset: QuerySet):
        melon_uid_list = queryset.values_list("melon_uid", flat=True)
        likes_dict = get_likes_dict(melon_uid_list)

        changed_count = 0

        for song in queryset:
            new_likes = likes_dict.get(song.melon_uid)
            if song.like_count != new_likes:
                song.like_count = likes_dict.get(song.melon_uid)
                changed_count += 1

        Song.objects.bulk_update(queryset, fields=["like_count"])

        self.message_user(request, message=f"{changed_count}곡의 좋아요 갱신 완료")
