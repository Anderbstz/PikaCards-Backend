from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

@api_view(['GET'])
def get_cards(request):
    url = "https://api.pokemontcg.io/v2/cards?page=1&pageSize=20"
    response = requests.get(url)
    return Response(response.json())

@api_view(["GET"])
def status(request):
    return Response({"status": "ok"})