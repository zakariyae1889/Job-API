import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr="iexact")
    keyword=django_filters.filterset.CharFilter(field_name="title",lookup_expr="icontains")
    minPrice=django_filters.filterset.NumberFilter(field_name="salary" or 0,lookup_expr="gte")
    maxPrice=django_filters.filterset.NumberFilter(field_name="salary" or 1000000, lookup_expr="lte")
    category__name=django_filters.filterset.CharFilter(field_name="category__name",lookup_expr="icontains")
    company__name=django_filters.filterset.CharFilter(field_name="company__name",lookup_expr="icontains")

    class Meta:
        model=Job
        fields=(
            "title",
            "category__name",
            "experience",
            "location",
            "company__name",
            "job_nature",
            "minPrice",
            "maxPrice",
            "posted_date"
        )