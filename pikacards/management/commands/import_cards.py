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

        total = 0

        for item in data:
            Card.objects.update_or_create(
                card_id=item["id"],
                defaults={
                    "name": item.get("name", ""),
                    "supertype": item.get("supertype", ""),
                    "subtypes": ",".join(item.get("subtypes", []))
                        if isinstance(item.get("subtypes"), list) else "",
                    "hp": item.get("hp", ""),
                    "types": ",".join(item.get("types", []))
                        if isinstance(item.get("types"), list) else "",
                    "rarity": item.get("rarity", ""),
                    "artist": item.get("artist", ""),
                    "set_id": item["set"]["id"] if "set" in item and "id" in item["set"] else "",
                    "image": item["images"]["small"] if "images" in item and "small" in item["images"] else "",
                }
            )
            total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Importación completa: {total} cartas cargadas"))
