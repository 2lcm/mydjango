from django.contrib import admin

from .models import Post, Tag, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ["author", "__str__", "slug"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass