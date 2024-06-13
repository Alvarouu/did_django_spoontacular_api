from django.urls import path
from . import views
from .views import LogOut, BusqAle

# 33389
app_name = "main"

urlpatterns = [

    path('', views.index, name="home"),
    path('results', views.results.as_view(), name="results"),
    path('add_to_shopping_list/<int:ingredient_id>/<str:ingredient_name>/', views.add_to_shopping_list,
         name='add_to_shopping_list'),
    path('shopping_list/', views.shopping_list.as_view(), name='shopping_list'),
    path('remove_one_from_shopping_list/<int:ingredient_id>/', views.remove_one_from_shopping_list,
         name='remove_one_from_shopping_list'),
    path('remove_all_from_shopping_list/<int:ingredient_id>/', views.remove_all_from_shopping_list,
         name='remove_all_from_shopping_list'),
    path('recipe_detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.Login.as_view(), name='login'),
    path('perfil/<int:pk>/', views.PerfilView.as_view(), name='perfil'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('recipe_detail_pdf/<int:recipe_id>', views.recipe_detail_pdf, name='recipe_pdf'),
    path('busqAle/', views.BusqAle.as_view(), name="busq_ale"),
    path('result_ale', views.result_ale.as_view(), name="result_ale")


]
