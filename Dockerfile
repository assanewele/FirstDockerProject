
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Installer les dépendances avec pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copier les fichiers de l'application
COPY ./app /code/app

# Exposer le port de l'API
EXPOSE 5000

CMD ["python", "app/app.py"]
