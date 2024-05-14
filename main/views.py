from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.shortcuts import HttpResponse
from django.contrib import messages


from .mixins import (
	FormErrors,
	RedirectParams,
	APIMixin
)
from .models import Ingredientes

'''
Basic view for selecting query
'''
def index(request):

	if request.method == "POST":
		cat = request.POST.get("cat", None)
		query = request.POST.get("query", None)
		if cat and query:
			return RedirectParams(url = 'main:results', params = {"cat": cat, "query": query})

	return render(request, 'main/index.html', {})



'''
Basic view for displaying results
'''
def results(request):

	cat = request.GET.get("cat", None)
	query = request.GET.get("query", None)

	if cat and query:
		results = APIMixin(cat=cat, query=query).get_data()

		if results:
			context = {
				"results": results,
				"cat": cat,
				"query": query,
			}

			return render(request, 'main/results.html', context)
	
	return redirect(reverse('main:home'))

def add_to_shopping_list(request, ingredient_id, ingredient_name):
    # Verifica si el ingrediente ya existe en la lista de la compra
    ingredient = Ingredientes.objects.filter(id=ingredient_id).first()

    if ingredient:
        # Si el ingrediente ya está en la lista, incrementa el contador
        ingredient.count += 1
        ingredient.save()
    else:
        # Si el ingrediente no está en la lista, crea un nuevo registro con el nombre real del ingrediente
        ingredient = Ingredientes.objects.create(id=ingredient_id, name=ingredient_name)
        ingredient.save()
    # Redirige a la página de la lista de la compra
    return redirect('main:shopping_list')

def shopping_list(request):
    ingredients = Ingredientes.objects.all()
    return render(request, 'main/shopping_list.html', {'ingredients': ingredients})

def remove_one_from_shopping_list(request, ingredient_id):
    # Obtener el ingrediente de la lista de compras
    ingredient = Ingredientes.objects.get(id=ingredient_id)

    # Decrementar la cantidad del ingrediente en uno
    if ingredient.count > 1:
        ingredient.count -= 1
        ingredient.save()
    else:
        # Si la cantidad es igual a uno, eliminar el ingrediente de la lista de compras
        ingredient.delete()

    # Redirigir a la página de la lista de compras
    return redirect('main:shopping_list')

def remove_all_from_shopping_list(request, ingredient_id):
    # Obtener el ingrediente de la lista de compras
    ingredient = Ingredientes.objects.get(id=ingredient_id)

    # Eliminar el ingrediente de la lista de compras
    ingredient.delete()

    # Redirigir a la página de la lista de compras
    return redirect('main:shopping_list')
