from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_401_UNAUTHORIZED)
        
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)



class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Sepeti al
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response({"error": "Sepet boş."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Siparişi oluştur
            total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount
            )

            # Sepet içeriğini siparişle ilişkilendir
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    color=item.color,
                    size=item.size,
                    quantity=item.quantity,
                    price=item.product.price
                )
                
            # Sepeti temizle
            cart.items.all().delete()
            
            return Response({"message": "Sipariş başarıyla oluşturuldu."}, status=status.HTTP_201_CREATED)
        
        except Cart.DoesNotExist:
            return Response({"error": "Sepet bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
