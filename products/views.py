# products/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Pagination Class
class ProductPagination(PageNumberPagination):
    page_size = 2

# Filter Class
class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='exact')
    color = filters.CharFilter(field_name='color', lookup_expr='exact')
    size = filters.CharFilter(field_name='size', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'color', 'size']

# Product List View
class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Apply filters and pagination
            products = Product.objects.all().order_by('-updated_at')  # Yeni: Sıralama
            filterset = ProductFilter(request.GET, queryset=products)
            if filterset.is_valid():
                filtered_products = filterset.qs
                paginator = ProductPagination()
                result_page = paginator.paginate_queryset(filtered_products, request)
                serializer = ProductSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            return Response({"error": filterset.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Product Detail View
class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Category List View
class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)