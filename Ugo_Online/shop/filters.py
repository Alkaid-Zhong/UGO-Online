from django_filters import rest_framework as filters
from .models import ShopTransaction

class ShopTransactionFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='date__date', lookup_expr='exact')
    # start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    # end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = ShopTransaction
        fields = ['transaction_type', 'date']
