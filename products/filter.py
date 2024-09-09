import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    size = django_filters.ChoiceFilter(choices=Product.SIZE_CHOICES)
    category = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='icontains')  # color filtresini ekledik

    class Meta:
        model = Product
        fields = ['size', 'category', 'color']  # Burada filtrelemek istediğiniz alanları belirtin
