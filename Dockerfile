# Utiliser Python 3.11.5
FROM python:3.11.5-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Exposer le port Django
EXPOSE 8000

# Commande par défaut pour lancer le serveur Django
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#production 
CMD ["gunicorn", "systeme_notification.wsgi:application", "--bind", "0.0.0.0:8000"]

