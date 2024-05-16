from typing import Any, List, Optional
from django.contrib import admin
from django.db.models import QuerySet
from django.db.models.functions import ExtractYear
from django.utils import timezone

from .models import Song


class ReleaseDateFilter(admin.SimpleListFilter):
    title = Song._meta.get_field("release_date").verbose_name
    parameter_name = "release_date_filter"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        year_list : List[int] = (
            Song.objects.annotate(year=ExtractYear("release_date"))
            .values_list("year", flat=True)
            .order_by("-year")
            .distinct()
        )

        fixed_lookups = [
            ("this_month", "이번 달")
        ]

        dynamic_lookups = [(year, f"{year}년") for year in year_list]

        return fixed_lookups + dynamic_lookups
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        value: Optional[str] = self.value()
        if value == "this_month":
            now = timezone.now()
            return queryset.filter(
                release_date__year=now.year,
                release_date__month=now.month
            )
        elif value is not None:
            return queryset.filter(release_date__year=value)
        return queryset
        