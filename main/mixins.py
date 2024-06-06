from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json


'''
Handles form error that are passed back to AJAX calls
'''
def FormErrors(*args):
	message = ""
	for f in args:
		if f.errors:
			message = f.errors.as_text()
	return message


'''
Used to append url parameters when redirecting users
'''
def RedirectParams(**kwargs):
	url = kwargs.get("url")
	params = kwargs.get("params")
	response = redirect(url)
	if params:
		query_string = urlencode(params)
		response['Location'] += '?' + query_string
	return response


class APIMixin:

	def __init__(self, *args, **kwargs):

		self.query = kwargs.get("query")
		self.cat = kwargs.get("cat")

	def get_recipe_information(self, recipe_id):
		url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={settings.API_KEY}"

		# Realizar la solicitud a la API
		response = requests.get(url)

		if 200 <= response.status_code <= 299:
			print(response.status_code)
			# Procesar la respuesta JSON
			data = response.json()
			print(data)
			return data
		else:
			# Manejar cualquier error de la solicitud
			print(f"Error al obtener la información de la receta: {response.status_code}")
			return None


	def get_data(self):

		url_dict = {
			"recipes": "recipes/complexSearch?",
			"ingredients": "food/ingredients/search?",
			"menuItems": "food/menuItems/search?",
			"products": "food/products/search?"
		}

		url = f"https://api.spoonacular.com/{url_dict[self.cat]}query={self.query}&apiKey={settings.API_KEY}"

		r = requests.get(url)
		if r.status_code == 200:
			try:
				return r.json()[self.cat]
			except KeyError:
				return r.json()['results']
		else:
			return None


# https://api.spoonacular.com/food/products/search?query=yogurt&apiKey=530a5f3b031f4576808837a1de7cce8c




