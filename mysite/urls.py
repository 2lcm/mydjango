from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls")),
    path("hottrack/", include("hottrack.urls")),
    path("blog/", include("blog.urls")),
    path("", lambda request : redirect("hottrack:index")),
]


if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
