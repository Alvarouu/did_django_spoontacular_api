from django.shortcuts import render, reverse, redirect
from django.db import transaction
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.views.generic import ListView, CreateView
from .forms import RegistroForm
from .mixins import (
    FormErrors,
    RedirectParams,
    APIMixin
)
from .models import Ingredientes, Perfil

'''
Basic view for selecting query
'''




def index(request):
    if request.method == "POST":
        cat = request.POST.get("cat", None)
        query = request.POST.get("query", None)
        if cat and query:
            # Genera la URL con los parámetros cat y query
            url = reverse('main:results') + f'?cat={cat}&query={query}'
            return redirect(url)

    return render(request, 'main/index.html', {})



class results(View):
    def get(self, request):
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
    try:
        # Obtener el perfil del usuario actual
        perfil, created = Perfil.objects.get_or_create(username=request.user)

        # Intentamos obtener el ingrediente del perfil del usuario
        ingredient = perfil.listaIng.filter(id=ingredient_id).first()

        if ingredient is not None:
            # Si el ingrediente ya existe en la lista de ingredientes del perfil, aumentamos su cantidad en uno
            ingredient.count += 1
            ingredient.save()
        else:
            # Si el ingrediente no existe en la lista de ingredientes del perfil, lo creamos con una cantidad de uno
            ingredient = Ingredientes.objects.create(id=ingredient_id, name=ingredient_name, count=1)
            perfil.listaIng.add(ingredient)

    except Exception as e:
        # Manejar cualquier otro error que pueda ocurrir
        print(f"Error: {e}")

    # Redireccionamos a la página de la lista de la compra
    return redirect('main:shopping_list')


def remove_one_from_shopping_list(request, ingredient_id):
    try:
        # Obtener el perfil del usuario autenticado
        perfil = Perfil.objects.get(username=request.user)

        # Obtener el ingrediente específico por su ID
        ingredient = perfil.listaIng.get(id=ingredient_id)

        if ingredient.count > 1:
            # Si el ingrediente tiene más de 1 en el count, reducirlo en 1
            ingredient.count -= 1
            ingredient.save()
        else:
            # Si solo hay 1 o menos, eliminar el ingrediente de la lista
            perfil.listaIng.remove(ingredient)

    except Exception as e:
        # Manejar cualquier otro error que pueda ocurrir
        print(f"Error: {e}")

    # Redirigir a la página de la lista de compras
    return redirect('main:shopping_list')


def remove_all_from_shopping_list(request, ingredient_id):
    try:
        # Obtener el perfil del usuario autenticado
        perfil = Perfil.objects.get(username=request.user)

        # Obtener el ingrediente de la lista de compras
        ingredient = perfil.listaIng.filter(id=ingredient_id).first()

        if ingredient is not None:
            # Si el ingrediente está en la lista de ingredientes del perfil, lo eliminamos
            perfil.listaIng.remove(ingredient)

    except Exception as e:
        # Manejar cualquier otro error que pueda ocurrir
        print(f"Error: {e}")

    # Redirigir a la página de la lista de compras
    return redirect('main:shopping_list')


def recipe_detail(request, recipe_id):
    api_client = APIMixin()  # Instancia del cliente API

    # Obtener la información detallada de la receta
    recipe_info = api_client.get_recipe_information(recipe_id)
    context = {
        "recipe_info": recipe_info
    }
    return render(request, 'main/recipe_detail.html', context)


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'main/registro.html'
    success_url = reverse_lazy('main:home')

    @transaction.atomic
    def get_template_names(self, request=None):
        return [self.template_name]


class Login(View):
    template_name = "login.html"
    form_class = AuthenticationForm

    def get(self, request):
        form = self.form_class()

        return render(request, 'main/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                id = user.pk

                return redirect('main:perfil', pk=user.id)

        form = AuthenticationForm()
        return render(request, 'main/login.html', {'form': form})


class shopping_list(LoginRequiredMixin, ListView):
    template_name = 'main/shopping_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el perfil del usuario actual
        perfil = Perfil.objects.get(username=self.request.user)

        # Obtener todos los ingredientes del perfil

        context['ingredients'] = perfil.listaIng.all()

        return context

    def get_queryset(self):
        # Filtra el perfil del usuario actual
        return Perfil.objects.filter(username=self.request.user)


class PerfilView(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'main/perfil.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        perfil = Perfil.objects.get(username=user)  # Utiliza el nombre real del campo
        context['user'] = user
        context['perfil'] = perfil
        context['alergenos'] = perfil.listaAle.all()
        print(context)
        print(perfil.listaAle.all())
        return context

    def get_queryset(self):
        # Filtra el perfil del usuario actual
        return Perfil.objects.filter(username=self.request.user)


class LogOut(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main:home'))