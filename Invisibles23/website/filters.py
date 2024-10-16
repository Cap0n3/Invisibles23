import django_filters
from .models import (
    AdminRessources,
    TherapeuticRessources,
    LibraryRessources,
)
from django.db.models import Q


class BaseRessourcesFilter(django_filters.FilterSet):
    """
    Base class for the ressources filters
    """

    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    keywords = django_filters.CharFilter(method="filter_keywords")

    def filter_keywords(self, queryset, name, value):
        print(f"fitering on {value.strip().split()}")
        if value:
            # Split the search queries by spaces
            searchQueries = value.strip().split()
            # create a Q object for each keyword
            q_objects = Q()
            for query in searchQueries:
                q_objects |= (
                    Q(keywords__icontains=query)
                    | Q(title__icontains=query)
                    | Q(description__icontains=query)
                )
            # filter the queryset
            queryset = queryset.filter(q_objects)
        return queryset

    class Meta:
        model = None
        fields = ["title", "description", "keywords"]


class AdminRessourcesFilter(BaseRessourcesFilter):
    class Meta(BaseRessourcesFilter.Meta):
        model = AdminRessources


class TherapeuticRessourcesFilter(BaseRessourcesFilter):
    class Meta(BaseRessourcesFilter.Meta):
        model = TherapeuticRessources


class LibraryRessourcesFilter(BaseRessourcesFilter):
    class Meta(BaseRessourcesFilter.Meta):
        model = LibraryRessources
