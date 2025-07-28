#!/usr/bin/env python
"""
Script de configuration initiale du projet LinguaChat AI
"""
import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Exécute une commande avec gestion d'erreur"""
    print(f"🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description} - Terminé")
        return True
    else:
        print(f"❌ {description} - Erreur: {result.stderr}")
        return False

def create_env_file():
    """Crée le fichier .env s'il n'existe pas"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Fichier .env créé à partir de .env.example")
            print("⚠️  N'oubliez pas de remplir vos clés API dans le fichier .env")
        else:
            print("❌ Fichier .env.example non trouvé")
    else:
        print("ℹ️  Le fichier .env existe déjà")

def setup_project():
    """Configuration complète du projet"""
    print("🚀 Configuration de LinguaChat AI")
    print("=" * 50)
    
    # Créer les dossiers nécessaires
    directories = ['static/css', 'static/js', 'media', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Dossier créé: {directory}")
    
    # Créer le fichier .env
    create_env_file()
    
    # Installation des dépendances
    if not run_command("pip install -r requirements.txt", "Installation des dépendances Python"):
        print("❌ Échec de l'installation des dépendances")
        return False
    
    # Migrations de base de données
    if not run_command("python manage.py makemigrations", "Création des migrations"):
        print("❌ Échec de la création des migrations")
        return False
    
    if not run_command("python manage.py migrate", "Application des migrations"):
        print("❌ Échec de l'application des migrations")
        return False
    
    # Collecte des fichiers statiques
    run_command("python manage.py collectstatic --noinput", "Collecte des fichiers statiques")
    
    # Création des données initiales
    run_command("python manage.py create_badges", "Création des badges initiaux")
    run_command("python manage.py create_challenges", "Création des défis initiaux")
    
    print("\n🎉 Configuration terminée!")
    print("\n📋 Prochaines étapes:")
    print("1. Configurez vos clés API dans le fichier .env")
    print("2. Créez un superutilisateur: python manage.py createsuperuser")
    print("3. Lancez le serveur: python manage.py runserver")
    print("4. Lancez Redis pour les WebSockets et Celery")
    print("5. Lancez Celery worker: celery -A linguachat worker -l info")
    print("6. Lancez Celery beat: celery -A linguachat beat -l info")
    
    return True

if __name__ == '__main__':
    setup_project()