from datetime import date
from typing import Any, Literal, Sequence
from urllib.request import urlopen

from django.conf import settings
from django.db.models import Q, QuerySet
from django.db.models.base import Model as Model
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic import ArchiveIndexView, DateDetailView, DayArchiveView, DetailView, ListView, MonthArchiveView, TodayArchiveView, WeekArchiveView, YearArchiveView

from hottrack.models import Song
from hottrack.utils.cover import make_cover_image

from io import BytesIO
import pandas as pd


class IndexView(ListView):
    model = Song
    template_name="hottrack/index.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()

        release_date = self.kwargs.get("release_date")
        if release_date:
            qs = qs.filter(release_date=release_date)

        query = self.request.GET.get("query", "").strip()

        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(artist__name__icontains=query)
                | Q(album__name__icontains=query)
            )

        qs = qs.select_related("artist")
        return qs

index = IndexView.as_view()


def cover_png(request, pk):
    # 최대값 512, 기본값 256
    canvas_size = min(512, int(request.GET.get("size", 256)))

    song = get_object_or_404(Song, pk=pk)

    cover_image = make_cover_image(
        song.cover_url, song.artist.name, canvas_size=canvas_size
    )

    response = HttpResponse(content_type="image/png")
    cover_image.save(response, format="png")

    return response


class SongDetailView(DetailView):
    model=Song


def export(request: HttpRequest, format: Literal["csv", "xlsx"]) -> HttpResponse:
    song_qs: QuerySet = Song.objects.all()

    # .values() : 지정한 필드로 구성된 사전 리스트를 반환
    song_qs = song_qs.values()
    # 원하는 필드만 지정해서 뽑을 수도 있습니다.
    # song_qs = song_qs.values("rank", "name", "artist_name", "like_count")

    # 사전 리스트를 인자로 받아서, DataFrame을 생성할 수 있습니다.
    df = pd.DataFrame(data=song_qs)

    # 메모리 파일 객체에 CSV 데이터를 저장합니다.
    # CSV를 HttpResponse에 바로 저장할 때 utf-8-sig 인코딩이 적용되지 않아서
    # BytesIO를 사용해서 인코딩을 적용한 후, HttpResponse에 저장합니다.
    export_file = BytesIO()

    if format == "csv":
        content_type = "text/csv"
        filename = "hottrack.csv"
        df.to_csv(path_or_buf=export_file, index=False, encoding="utf-8-sig")  # noqa
    elif format == "xlsx":
        # .xls : application/vnd.ms-excel
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # xlsx
        )
        filename = "hottrack.xlsx"
        df.to_excel(excel_writer=export_file, index=False, engine="openpyxl")  # noqa
    else:
        return HttpResponseBadRequest(f"Invalid format : {format}")

    # 저장된 파일의 전체 내용을 HttpResponse에 전달합니다.
    response = HttpResponse(content=export_file.getvalue(), content_type=content_type)
    response["Content-Disposition"] = f"attachment; filename*=utf-8''{filename}"

    return response


class SongYearArchiveView(YearArchiveView):
    model = Song
    date_field = "release_date"
    make_object_list = True


class SongMonthArchiveView(MonthArchiveView):
    model = Song
    date_field = "release_date"
    month_format = "%m"


class SongDayArchiveView(DayArchiveView):
    model = Song
    date_field = "release_date"
    month_format = "%m"


class SongTodayArchiveView(TodayArchiveView):
    model = Song
    date_field = "release_date"

    if settings.DEBUG:
        def get_dated_items(self) -> tuple[Sequence[date] | None, Sequence[object], dict[str, Any]]:
            fake_today = self.request.GET.get("fake-today", "")
            try:
                year, month, day = map(int, fake_today.split("-", 3))
                return self._get_dated_items(date(year, month, day))
            except ValueError:
                return super().get_dated_items()


class SongWeekArchiveView(WeekArchiveView):
    model = Song
    date_field = "release_date"
    week_format = "%W"



class SongArchiveIndexView(ArchiveIndexView):
    model = Song
    date_field = "release_date"
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["date_list_period"] = self.get_date_list_period()
        return context_data

    def get_date_list_period(self) -> str:
        return self.kwargs.get("date_list_period", self.date_list_period)


class SongDateDetailView(DateDetailView):
    model = Song
    date_field = "release_date"
    month_format = "%m"