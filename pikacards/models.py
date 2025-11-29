from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class Card(models.Model):
    card_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    supertype = models.CharField(max_length=50)
    subtypes = models.CharField(max_length=200, blank=True)
    hp = models.CharField(max_length=10, blank=True)
    types = models.CharField(max_length=200, blank=True)
    rarity = models.CharField(max_length=50, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    set_id = models.CharField(max_length=50, blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)
    product_id = models.IntegerField()  # ID del producto real
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # precio unitario

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.card.name} x {self.quantity}"