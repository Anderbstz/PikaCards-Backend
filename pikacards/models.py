from django.db import models

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