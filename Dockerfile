FROM python:3.11-slim

WORKDIR /usr/app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY . .

# Configurar y exponer la aplicación
EXPOSE 9000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:9000", "--settings=did_django_spoontacular_api.settings" ]
