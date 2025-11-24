from django.urls import path
from . import views

urlpatterns = [
    path("status/", views.status),
    path("cards/", views.get_cards),  # nuevo
]