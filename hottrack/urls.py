from django.urls import include, path, re_path, register_converter

from hottrack import converters
from hottrack import views

register_converter(converters.DateConverter, "date")
app_name = "hottrack"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.SongDetailView.as_view(), name="song_detail"),
    path("melon-<int:melon_uid>/", views.SongDetailView.as_view(), name="song_detail"),
    # path("archives/<date:release_date>/", views.index),
    path("archives/today/", views.SongTodayArchiveView.as_view(), name="song_archive_today"),
    path("archives/<int:year>/", views.SongYearArchiveView.as_view(), name="song_archive_year"),
    path("archives/<int:year>/<int:month>", views.SongMonthArchiveView.as_view(), name="song_archive_month"),
    path("archives/<int:year>/<int:month>/<int:day>", views.SongDayArchiveView.as_view(), name="song_archive_day"),
    path("archives/<int:year>/week/<int:week>", views.SongWeekArchiveView.as_view(), name="song_archive_week"),
    # path("<int:year>/<int:month>/<int:day>/<int:pk>", views.SongDateDetailView.as_view(), name="song_date_detail"),
    re_path(r"^archives/(?P<date_list_period>(year|month|day|week)?/?)", views.SongArchiveIndexView.as_view(), name="song_archive_index"),
    re_path(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$", views.SongDateDetailView.as_view(), name="song_detail"),
    re_path(r"^export\.(?P<format>(csv|xlsx))$", views.export, name="export"),
    path("<int:pk>/cover.png", views.cover_png, name="cover_png"),
]
