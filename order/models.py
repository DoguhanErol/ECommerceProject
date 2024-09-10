from django.db import models
from django.conf import settings
from cart.models import Cart
from products.models import Product
from django.contrib.auth.models import User  

class Order(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Hazırlanıyor'),
        ('shipped', 'Kargoya Verildi'),
        ('completed', 'Tamamlandı'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='preparing')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=2)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} adet"
