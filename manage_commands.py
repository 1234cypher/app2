#!/usr/bin/env python
"""
Script pour exécuter les commandes de gestion Django courantes
"""
import os
import sys
import subprocess

def run_command(command):
    """Exécute une commande et affiche le résultat"""
    print(f"Exécution de: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Erreur: {result.stderr}")
    return result.returncode == 0

def main():
    """Menu principal pour les commandes de gestion"""
    commands = {
        '1': ('Créer les migrations', 'python manage.py makemigrations'),
        '2': ('Appliquer les migrations', 'python manage.py migrate'),
        '3': ('Créer un superutilisateur', 'python manage.py createsuperuser'),
        '4': ('Collecter les fichiers statiques', 'python manage.py collectstatic --noinput'),
        '5': ('Créer les badges initiaux', 'python manage.py create_badges'),
        '6': ('Créer les défis initiaux', 'python manage.py create_challenges'),
        '7': ('Lancer le serveur de développement', 'python manage.py runserver'),
        '8': ('Lancer Celery worker', 'celery -A linguachat worker -l info'),
        '9': ('Lancer Celery beat', 'celery -A linguachat beat -l info'),
        '10': ('Installer les dépendances', 'pip install -r requirements.txt'),
    }
    
    print("=== LinguaChat AI - Commandes de gestion ===")
    print()
    for key, (description, _) in commands.items():
        print(f"{key}. {description}")
    print("0. Quitter")
    print()
    
    while True:
        choice = input("Choisissez une option (0-10): ").strip()
        
        if choice == '0':
            print("Au revoir!")
            break
        elif choice in commands:
            description, command = commands[choice]
            print(f"\n--- {description} ---")
            success = run_command(command)
            if success:
                print("✅ Commande exécutée avec succès!")
            else:
                print("❌ Erreur lors de l'exécution de la commande")
            print()
        else:
            print("Option invalide. Veuillez choisir entre 0 et 10.")

if __name__ == '__main__':
    main()