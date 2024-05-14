from django.urls import path
from . import views

#33389
app_name = "main"

urlpatterns = [
	
	path('', views.index, name="home"),
	path('results', views.results, name="results"),
	path('add_to_shopping_list/<int:ingredient_id>/<str:ingredient_name>/', views.add_to_shopping_list, name='add_to_shopping_list'),
	path('shopping_list/', views.shopping_list, name='shopping_list'),
	path('remove_one_from_shopping_list/<int:ingredient_id>/', views.remove_one_from_shopping_list, name='remove_one_from_shopping_list'),
    path('remove_all_from_shopping_list/<int:ingredient_id>/', views.remove_all_from_shopping_list, name='remove_all_from_shopping_list'),
	]