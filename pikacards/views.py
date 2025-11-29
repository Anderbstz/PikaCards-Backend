import stripe
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from pikacards.models import Card

stripe.api_key = settings.STRIPE_SECRET_KEY

# ----------------------------------------
# 0. Estado
# ----------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def status(request):
    return Response({"status": "ok"})


# ----------------------------------------
# 1. Listado general (local)
# ----------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def get_cards(request):
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("pageSize", 20))

    start = (page - 1) * page_size
    end = start + page_size

    # Ordenamos por id descendente para priorizar cartas reales importadas
    cards_qs = Card.objects.order_by("-id")
    cards = cards_qs[start:end]
    total = cards_qs.count()

    data = [
        {
            "id": c.card_id,
            "name": c.name,
            "types": c.types.split(",") if c.types else [],
            "rarity": c.rarity,
            "image": c.image,
            "artist": c.artist,
            "set_id": c.set_id,
            "hp": c.hp,
        }
        for c in cards
    ]

    return Response({
        "page": page,
        "pageSize": page_size,
        "total": total,
        "results": data
    })


# ----------------------------------------
# 2. Búsqueda simple (local)
# ----------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def search_cards(request):
    query = request.GET.get("q", "").lower()

    if not query:
        return Response({"error": "La búsqueda está vacía"}, status=400)

    cards = Card.objects.filter(name__icontains=query)

    data = [
        {
            "id": c.card_id,
            "name": c.name,
            "types": c.types.split(",") if c.types else [],
            "rarity": c.rarity,
            "image": c.image,
            "artist": c.artist,
            "set_id": c.set_id,
            "hp": c.hp,
        }
        for c in cards
    ]

    return Response(data)


# ----------------------------------------
# 3. Búsqueda avanzada (local)
# ----------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def search_cards_advanced(request):
    name = request.GET.get("name")
    artist = request.GET.get("artist")
    type_ = request.GET.get("type")
    rarity = request.GET.get("rarity")
    set_ = request.GET.get("set")

    qs = Card.objects.all()

    if name:
        qs = qs.filter(name__icontains=name)

    if artist:
        qs = qs.filter(artist__icontains=artist)

    if type_:
        qs = qs.filter(types__icontains=type_)

    if rarity:
        qs = qs.filter(rarity__icontains=rarity)

    if set_:
        qs = qs.filter(set_id__icontains=set_)

    data = [
        {
            "id": c.card_id,
            "name": c.name,
            "types": c.types.split(",") if c.types else [],
            "rarity": c.rarity,
            "image": c.image,
            "artist": c.artist,
            "set_id": c.set_id,
            "hp": c.hp,
        }
        for c in qs
    ]

    return Response(data)


# ----------------------------------------
# 4. Submenús (locales)
# ----------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def search_by_type(request, type):
    cards = Card.objects.filter(types__icontains=type)

    data = [
        { "id": c.card_id, "name": c.name, "image": c.image }
        for c in cards
    ]

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_by_rarity(request, rarity):
    cards = Card.objects.filter(rarity__icontains=rarity)

    data = [
        { "id": c.card_id, "name": c.name, "image": c.image }
        for c in cards
    ]

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_by_set(request, set_id):
    cards = Card.objects.filter(set_id__icontains=set_id)

    data = [
        { "id": c.card_id, "name": c.name, "image": c.image }
        for c in cards
    ]

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_by_artist(request, artist):
    cards = Card.objects.filter(artist__icontains=artist)

    data = [
        { "id": c.card_id, "name": c.name, "image": c.image }
        for c in cards
    ]

    return Response(data)
@api_view(["GET"])
@permission_classes([AllowAny])
def card_detail(request, card_id):
    try:
        from pikacards.models import Card
        c = Card.objects.get(card_id=card_id)

        data = {
            "id": c.card_id,
            "name": c.name,
            "supertype": c.supertype,
            "subtypes": c.subtypes.split(",") if c.subtypes else [],
            "hp": c.hp,
            "types": c.types.split(",") if c.types else [],
            "rarity": c.rarity,
            "artist": c.artist,
            "set_id": c.set_id,
            "image": c.image,
        }

        return Response(data)
    except Card.DoesNotExist:
        return Response({"error": "Card not found"}, status=404)

@api_view(["GET"])
@permission_classes([AllowAny])
def filter_cards(request):
    qs = Card.objects.all()

    # Filtros opcionales
    if "name" in request.GET:
        qs = qs.filter(name__icontains=request.GET["name"])

    if "type" in request.GET:
        qs = qs.filter(types__icontains=request.GET["type"])

    if "rarity" in request.GET:
        qs = qs.filter(rarity__icontains=request.GET["rarity"])

    if "artist" in request.GET:
        qs = qs.filter(artist__icontains=request.GET["artist"])

    if "set" in request.GET:
        qs = qs.filter(set_id__icontains=request.GET["set"])

    data = [
        {
            "id": c.card_id,
            "name": c.name,
            "types": c.types.split(",") if c.types else [],
            "rarity": c.rarity,
            "image": c.image,
            "artist": c.artist,
            "set_id": c.set_id,
            "hp": c.hp,
        }
        for c in qs
    ]

    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def list_types(request):
    from django.db.models import Value
    cards = Card.objects.exclude(types="")

    types = set()
    for c in cards:
        for t in c.types.split(","):
            types.add(t.strip())

    return Response(sorted(list(types)))

@api_view(["GET"])
@permission_classes([AllowAny])
def list_rarities(request):
    rarities = (
        Card.objects.exclude(rarity="")
        .values_list("rarity", flat=True)
        .distinct()
    )
    return Response(sorted(list(rarities)))

@api_view(["GET"])
@permission_classes([AllowAny])
def list_sets(request):
    sets = (
        Card.objects.exclude(set_id="")
        .values_list("set_id", flat=True)
        .distinct()
    )
    return Response(sorted(list(sets)))

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    cart = request.data.get("cart", [])

    if not cart:
        return Response({"error": "Carrito vacío"}, status=400)

    # Validación temprana de configuración de Stripe para evitar errores HTML (500)
    if not getattr(settings, "STRIPE_SECRET_KEY", None):
        return Response({"error": "Stripe no está configurado en el servidor"}, status=500)

    try:
        line_items = []

        for item in cart:
            # Construir product_data sin imágenes vacías
            product_data = {"name": item["name"]}
            image_url = item.get("image")
            if image_url:
                product_data["images"] = [image_url]

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": product_data,
                    "unit_amount": int(float(item["price"]) * 100),
                },
                "quantity": item["quantity"],
            })

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )

        return Response({"url": session.url})
    except Exception as e:
        # Siempre devolver JSON para que el frontend no intente parsear HTML
        return Response({"error": f"Error al inicializar el pago: {str(e)}"}, status=500)