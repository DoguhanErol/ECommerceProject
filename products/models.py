# products/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Boş geçilebilir
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, default='unknown')
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='M')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
