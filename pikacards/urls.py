from django.urls import path
from . import views
from pikacards.views import purchase_history
from .views import (
    create_checkout_session,
    stripe_webhook,
    add_to_cart, get_cart, remove_from_cart,
    purchase_history
)
from .views import add_to_cart, get_cart, remove_from_cart, create_checkout_session, purchase_history
from .views import create_billing_portal_session
urlpatterns = [
    # Estado
    path("status/", views.status),

    # Listado general
    path("cards/", views.get_cards),

    # Búsqueda simple
    path("cards/search/", views.search_cards),

    # Búsqueda avanzada
    path("cards/search/advanced/", views.search_cards_advanced),

    # Submenús ESPECÍFICOS
    path("cards/type/<str:type>/", views.search_by_type),
    path("cards/rarity/<str:rarity>/", views.search_by_rarity),
    path("cards/set/<str:set_id>/", views.search_by_set),
    path("cards/artist/<str:artist>/", views.search_by_artist),

    # Filtro general
    path("cards/filter/", views.filter_cards),

    # Listados únicos
    path("cards/types/", views.list_types),
    path("cards/rarities/", views.list_rarities),
    path("cards/sets/", views.list_sets),

    # 👇 ESTA SIEMPRE AL FINAL
    path("cards/<str:card_id>/", views.card_detail),
    
    path("cart/checkout/", views.create_checkout_session),
    
    path("api/history/", purchase_history, name="purchase-history"),

    path("cart/", get_cart),
    path("cart/add/", add_to_cart),
    path("cart/remove/<int:item_id>/", remove_from_cart),

    path("checkout/", create_checkout_session),
    path("history/", purchase_history),

    path("webhook/stripe/", stripe_webhook),
    path("billing/portal/", create_billing_portal_session),
]
