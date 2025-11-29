import stripe
from django.conf import settings
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User

from pikacards.models import Card, Order, OrderItem, CartItem
from .serializers import OrderSerializer, CartItemSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# Precio pseudo-determinístico similar al frontend para datos consistentes
def get_card_price(card: Card):
    seed = (card.card_id or card.name or "pikacards")
    hash_value = sum(ord(ch) * (i + 1) for i, ch in enumerate(seed))
    pseudo = 5 + (hash_value % 100) / 5  # 5 a 25
    return round(pseudo, 2)

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
            success_url="http://localhost:5173/history?success=1",
            cancel_url="http://localhost:5173/cancel",
        )

        return Response({"url": session.url})
    except Exception as e:
        # Siempre devolver JSON para que el frontend no intente parsear HTML
        return Response({"error": f"Error al inicializar el pago: {str(e)}"}, status=500)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def purchase_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    card_id = request.data.get("card_id")

    try:
        card = Card.objects.get(card_id=card_id)
    except Card.DoesNotExist:
        return Response({"error": "Card not found"}, status=404)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        card=card,
    )

    if not created:
        item.quantity += 1
        item.save()

    return Response({"message": "Added to cart"})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, user=request.user)
        item.delete()
        return Response({"message": "Item removed"})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)
    
def clear_cart(user):
    CartItem.objects.filter(user=user).delete()
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    line_items = []

    for item in cart_items:
        unit_price = get_card_price(item.card)
        line_items.append({
            "price_data": {
                "currency": "pen",
                "product_data": {
                    "name": item.card.name,
                },
                "unit_amount": int(round(unit_price * 100)),
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=line_items,
        success_url="http://localhost:5173/history?success=1",
        cancel_url="http://localhost:5173/cancel",
        customer_email=request.user.email,
        client_reference_id=str(request.user.id),
    )

    return Response({"url": session.url})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_billing_portal_session(request):
    """Crea una sesión del portal de facturación de Stripe para que el usuario
    gestione sus métodos de pago. Se busca/crea el Customer por email.
    """
    try:
        # Buscar cliente por email
        customers = stripe.Customer.list(email=request.user.email, limit=1)
        if customers.data:
            customer_id = customers.data[0].id
        else:
            customer = stripe.Customer.create(email=request.user.email)
            customer_id = customer.id

        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url="http://localhost:5173/profile",
        )
        return Response({"url": portal_session.url})
    except Exception as e:
        return Response({"error": f"Error al abrir el portal de pagos: {str(e)}"}, status=500)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        else:
            event = json.loads(payload)
    except Exception:
        return HttpResponse(status=400)

    if event.get("type") == "checkout.session.completed":
        session = event["data"]["object"]

        # Preferir client_reference_id (ID de usuario) y hacer fallback al email
        user = None
        user_id = session.get("client_reference_id")
        if user_id:
            try:
                user = User.objects.get(id=int(user_id))
            except (User.DoesNotExist, ValueError):
                user = None

        if user is None:
            email = (session.get("customer_details") or {}).get("email") or session.get("customer_email")
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = None

        # Si no podemos vincular el usuario, regresamos 200 para evitar reintentos
        if user is None:
            return HttpResponse(status=200)

        cart_items = CartItem.objects.filter(user=user)

        order = Order.objects.create(
            user=user,
            total=0
        )

        total = 0

        for item in cart_items:
            unit_price = get_card_price(item.card)
            OrderItem.objects.create(
                order=order,
                product_name=item.card.name,
                product_id=item.card.id,
                quantity=item.quantity,
                price=unit_price
            )
            total += item.quantity * unit_price

        order.total = total
        order.save()

        clear_cart(user)

    return HttpResponse(status=200)