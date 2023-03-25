import django_filters
from django_filters import DateFilter
from .models import *

class MemberFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = "__all__"
