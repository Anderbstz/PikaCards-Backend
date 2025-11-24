from django.urls import path
from . import views

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
]
