from rest_framework import serializers
from .models import Order, OrderItem, CartItem, Card

class OrderItemSerializer(serializers.ModelSerializer):
    # Campos derivados para enriquecer el historial
    product_image = serializers.SerializerMethodField()
    product_card_id = serializers.SerializerMethodField()

    def get_product_image(self, obj):
        try:
            card = Card.objects.get(id=obj.product_id)
            return card.image
        except Card.DoesNotExist:
            return ""

    def get_product_card_id(self, obj):
        try:
            card = Card.objects.get(id=obj.product_id)
            return card.card_id
        except Card.DoesNotExist:
            return None

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product_name",
            "product_id",
            "quantity",
            "price",
            "product_image",
            "product_card_id",
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    card_name = serializers.CharField(source="card.name", read_only=True)
    card_image = serializers.CharField(source="card.image", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "card", "card_name", "card_image", "quantity"]