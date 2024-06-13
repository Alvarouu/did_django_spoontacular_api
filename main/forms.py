from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Perfil, Alergenos
from django.contrib.auth.forms import AuthenticationForm


class RegistroForm(UserCreationForm):
    alergenos = forms.ModelMultipleChoiceField(
        queryset=Alergenos.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear el perfil
            user_profile = Perfil.objects.create(
                username=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email']
            )
            # Establecer los alérgenos seleccionados y marcar el campo is_selected como True
            selected_allergens = self.cleaned_data['alergenos']
            for alergeno in selected_allergens:
                alergeno.is_selected = True
                alergeno.save()
            user_profile.listaAle.set(selected_allergens)
            user_profile.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['password', 'username']



