from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Alergenos


@receiver(post_migrate)
def populate_allergens(sender, **kwargs):
    initial_allergens = [
        'apio', 'gluten', 'crustáceos', 'huevos', 'pescado', 'altramuz',
        'leche', 'moluscos', 'mostaza', 'maní', 'sésamo', 'soja',
        'dióxido de azufre y sulfitos', 'frutos secos'
    ]
    for allergen in initial_allergens:
        Alergenos.objects.get_or_create(name=allergen)

