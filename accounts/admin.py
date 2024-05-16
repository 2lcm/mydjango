from django.contrib import admin

from .models import Profile, SuperUser, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass