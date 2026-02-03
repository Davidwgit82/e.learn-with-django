Booking Course System
Une plateforme de gestion et de réservation de cours en ligne développée avec Django 6.0. Le système permet aux professeurs de proposer des cours et aux étudiants de s'inscrire en un clic, tout en gérant automatiquement la disponibilité des places.

🚀 Fonctionnalités
Gestion des Cours : Création, modification et suppression de cours avec catégories et professeurs.

Système de Disponibilité : Calcul en temps réel des places restantes.

Contrôle Administratif : Possibilité de suspendre les inscriptions manuellement (is_active).

Réservations : Système d'inscription sécurisé pour les étudiants connectés.

Interface Admin Pro : Dashboard personnalisé avec filtres, recherche et indicateurs visuels (SOLD OUT, Dispo).

SEO Friendly : Utilisation de slugs pour des URLs de cours lisibles.

🛠 Tech Stack
Backend : Python 3.13, Django 6.0

Frontend : Django Templates, Tailwind CSS (pour le styling)

Database : SQLite (par défaut pour le développement)

📋 Prérequis
Python 3.13+

Virtualenv

⚙️ Installation
Cloner le projet

Bash
git clone <ton-url-de-repo>
cd booking-course
Créer et activer l'environnement virtuel

Bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
Installer les dépendances

Bash
pip install django
Migrations et Database

Bash
python manage.py makemigrations
python manage.py migrate
Créer un superutilisateur (Admin)

Bash
python manage.py createsuperuser
Lancer le serveur

Bash
python manage.py runserver
📸 Aperçu du Modèle de Données
Le projet repose sur trois piliers principaux :

Course : Le cœur du système (titre, prix, places, état).

Category : Organisation des cours par thématique.

Reservation : Table de liaison entre User (étudiant) et Course.
