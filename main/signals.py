from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Alergenos


@receiver(post_migrate)
def populate_allergens(sender, **kwargs):
    initial_allergens = [
        'celery', 'gluten', 'crustaceans', 'egg', 'fish', 'lupine',
        'milk', 'mollusks', 'mustard', 'peanut', 'sesame', 'soy',
        'sulfur dioxide and sulfites', 'nuts'
    ]
    for allergen in initial_allergens:
        Alergenos.objects.get_or_create(name=allergen)

