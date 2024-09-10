# orders/urls.py
from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView

urlpatterns = [
    path('list/', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
]
