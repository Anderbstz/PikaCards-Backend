import requests
from django.http import JsonResponse


def status(request):
    return JsonResponse({"message": "API de PikaCards funcionando!"})

def get_cards(request):
    url = "https://api.pokemontcg.io/v2/cards?pageSize=12"
    response = requests.get(url)
    data = response.json()

    # Solo mandamos las cartas, sin metadatos
    return JsonResponse(data, safe=False)