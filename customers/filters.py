import django_filters

from .models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    email = django_filters.CharFilter(
        field_name="email",
        lookup_expr="icontains",
    )

    national_id = django_filters.CharFilter(
        field_name="national_id",
        lookup_expr="icontains",
    )

    created_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    created_to = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    class Meta:
        model = Customer
        fields = [
            "name",
            "status",
            "email",
            "national_id",
            "created_from",
            "created_to",
        ]