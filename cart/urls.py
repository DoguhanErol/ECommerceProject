from django.urls import path
from .views import CartView, AddToCartView, CartRemoveView, CartClearView

urlpatterns = [
    path('list/', CartView.as_view(), name='cart-list'),
    path('add/', AddToCartView.as_view(), name='cart-add'),
    path('remove/', CartRemoveView.as_view(), name='cart-remove'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
]
