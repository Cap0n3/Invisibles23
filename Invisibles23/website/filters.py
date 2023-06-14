import django_filters
from .models import (
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
)
from django.db.models import Q

class AdminRessourcesFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method='filter_keywords')

    def filter_keywords(self, queryset, name, value):
        print(f"fitering on {value}")
        if value:
            # split the keywords by comma
            keywordsList = value.split(',')
            # create a Q object for each keyword
            q_objects = Q()
            for keyword in keywordsList:
                q_objects |= Q(keywords__icontains=keyword)
            queryset = queryset.filter(q_objects)
        return queryset
            
    class Meta:
        model = AdminRessources
        fields = ['keywords']
    