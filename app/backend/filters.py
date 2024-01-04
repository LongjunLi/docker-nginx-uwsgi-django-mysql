from django_filters import rest_framework as filters

from backend.models import *


class ItemFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Item
        fields = ("name",)
