import json
from pathlib import Path
from django.core.management.base import BaseCommand
from pikacards.models import Card

class Command(BaseCommand):
    help = "Importa cartas desde cards_500.json"

    def handle(self, *args, **kwargs):
        json_path = Path("pikacards/data/cards_500.json")

        if not json_path.exists():
            self.stdout.write(self.style.ERROR("❌ No se encontró cards_500.json en pikacards/data/"))
            return

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Detecta las posibles estructuras del JSON y normaliza a una lista
        if isinstance(data, dict):
            if "cards" in data and isinstance(data["cards"], list):
                items = data["cards"]
            elif "data" in data and isinstance(data["data"], list):
                items = data["data"]
            else:
                # Si es un dict pero no está en las claves esperadas, no hay nada que importar
                items = []
        elif isinstance(data, list):
            items = data
        else:
            items = []

        total = 0

        for item in items:
            # Compatibilidad con distintas versiones de esquema
            card_id = item.get("id", "")
            name = item.get("name", "")
            supertype = item.get("supertype", "")

            # subtypes puede venir como "subtypes" (lista) o "subtype" (string)
            raw_subtypes = item.get("subtypes")
            if isinstance(raw_subtypes, list):
                subtypes = ",".join(raw_subtypes)
            else:
                subtypes = item.get("subtype", "")

            hp = item.get("hp", "")

            # types siempre lista en la mayoría de datasets
            raw_types = item.get("types", [])
            types = ",".join(raw_types) if isinstance(raw_types, list) else str(raw_types or "")

            rarity = item.get("rarity", "")
            artist = item.get("artist", "")

            # set id puede venir como setCode (string) o set.id (objeto)
            set_id = item.get("setCode") or (
                item.get("set", {}).get("id") if isinstance(item.get("set"), dict) else ""
            ) or item.get("set", "")

            # imagen puede venir como imageUrl (string) o images.small
            image = item.get("imageUrl") or (
                item.get("images", {}).get("small") if isinstance(item.get("images"), dict) else ""
            ) or item.get("image", "")

            if not card_id:
                # Si no hay id, saltamos para evitar conflictos de clave única
                continue

            Card.objects.update_or_create(
                card_id=card_id,
                defaults={
                    "name": name,
                    "supertype": supertype,
                    "subtypes": subtypes,
                    "hp": hp,
                    "types": types,
                    "rarity": rarity,
                    "artist": artist,
                    "set_id": set_id,
                    "image": image,
                }
            )
            total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Importación completa: {total} cartas cargadas"))
