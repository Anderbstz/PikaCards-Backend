from django.core.management.base import BaseCommand
from pikacards.models import Card


class Command(BaseCommand):
    help = "Elimina cartas dummy (Pokemon 1..n) y registros sin imagen"

    def handle(self, *args, **kwargs):
        # Criterios de dummy: nombre empieza con 'Pokemon ' y card_id generado tipo 'card-...', sin imagen
        dummy_qs = Card.objects.filter(name__startswith="Pokemon ", image="", card_id__startswith="card-")
        no_image_qs = Card.objects.filter(image="")

        dummy_count = dummy_qs.count()
        no_image_count = no_image_qs.count()

        # Primero elimina los dummy específicos
        dummy_qs.delete()

        # Luego elimina el resto sin imagen (si aún existen)
        # Evita borrar si coinciden con los que ya fueron eliminados
        no_image_qs.delete()

        self.stdout.write(self.style.SUCCESS(
            f"✅ Limpieza completa: {dummy_count} dummy y {no_image_count} sin imagen eliminados"
        ))