import django_filters
from .models import Categories
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="iexact")
    keyword = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Categories
        fields = ("name",)
