# **MeetingPro**

MeetingPro est une application de gestion de réservations de salles, développée en Python avec une interface graphique basée sur `tkinter`. Elle permet aux utilisateurs de gérer les clients, les salles, et les réservations de manière intuitive et efficace.

---

## **Table des matières**
1. [Fonctionnalités](#fonctionnalités)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Structure du projet](#structure-du-projet)
6. [Détails des fichiers](#détails-des-fichiers)
7. [Contributeurs](#contributeurs)
8. [Licence](#licence)

---

## **Fonctionnalités**

### **1. Gestion des clients**
- Ajouter un nouveau client avec son nom, prénom et email.
- Afficher la liste des clients enregistrés.

### **2. Gestion des salles**
- Ajouter une salle avec un nom unique, un type (Standard, Conférence, Informatique) et une capacité.
- Afficher la liste des salles disponibles.

### **3. Réservations**
- Réserver une salle pour un client sur un créneau horaire spécifique.
- Afficher les salles disponibles pour un créneau donné.
- Afficher les réservations d'un client spécifique.

### **4. Interface utilisateur intuitive**
- Interface en français avec des boutons clairs et des formulaires simples.
- Navigation facile entre les différentes sections : Accueil, Ajouter, Réserver, Afficher.

### **5. Journalisation**
- Utilisation du module `logging` pour suivre les actions importantes et les erreurs dans la console.

---

## **Prérequis**

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

1. **Python 3.10 ou supérieur** : Téléchargez-le depuis [python.org](https://www.python.org/).
2. **Modules Python nécessaires** :
   - `tkinter` (inclus par défaut avec Python)
   - `tkcalendar`
   - `logging`

---

## **Installation**

1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/EngS1/Projet_CEREN_SYLLA.git
   cd Projet_CEREN_SYLLA
   ```
2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

---

## **Utilisation**

1. Exécutez l'application :
   ```bash
   python src/main.py
   ```
2. Interface principale :
   - **Accueil** : Vue d'ensemble des réservations et des salles.
   - **Ajouter** : Formulaires pour ajouter un client ou une salle.
   - **Réserver** : Interface pour réserver une salle pour un client.
   - **Afficher** : Consultation des réservations et des disponibilités.

---

## **Structure du projet**

Voici la structure détaillée du projet :

```
Projet_CEREN_SYLLA
├── src
│   ├── gui.py                # Interface graphique développée avec Tkinter
│   ├── main.py               # Logique principale du projet
│   ├── controller.py         # Contrôleur pour gérer les interactions entre la vue et le modèle
│   ├── model.py              # Modèle pour gérer les données et la logique métier
│   ├── database.py           # Gestion des données (lecture/écriture dans data.json)
│   ├── utils.py              # Fonctions utilitaires réutilisables
│   └── __init__.py           # Permet de traiter le dossier comme un package Python
├── tests
│   ├── test_main.py          # Tests unitaires pour les fonctions de main.py
│   ├── test_gui.py           # Tests unitaires pour l'interface graphique
│   ├── test_controller.py    # Tests unitaires pour le contrôleur
│   ├── test_model.py         # Tests unitaires pour le modèle
│   ├── test_database.py      # Tests unitaires pour la gestion des données
│   └── __init__.py           # Permet de traiter le dossier comme un package Python
├── data.json                 # Fichier JSON pour stocker les données
├── requirements.txt          # Liste des dépendances nécessaires
├── pyproject.toml            # Configuration du projet
├── lancer_application.bat    # Script pour lancer l'application sur Windows
├── README.md                 # Documentation complète du projet
└── .gitignore                # Fichier pour ignorer certains fichiers/dossiers dans Git
```

## **Détails des fichiers**

### 1. **Dossier `src`**
Ce dossier contient tout le code source de l'application.

- **`main.py`**  
  Contient la logique principale du projet. Ce fichier inclut les fonctions nécessaires pour exécuter les calculs ou les traitements principaux.  
  **Exemple de fonctions :**
  - `def some_function():` : Une fonction de base pour effectuer une tâche spécifique.
  - `def process_data(data):` : Traite les données reçues de l'interface graphique.

- **`gui.py`**  
  Contient l'interface graphique développée avec Tkinter. Ce fichier gère l'affichage, les interactions utilisateur et la communication avec le backend.  
  **Exemple de fonctionnalités :**
  - Boutons pour exécuter des actions.
  - Champs de saisie pour entrer des données.
  - Affichage des résultats.

- **`controller.py`**  
  Gère les interactions entre la vue (interface graphique) et le modèle (logique métier, données). Ce fichier contient les fonctions qui répondent aux actions de l'utilisateur et mettent à jour l'affichage en conséquence.

- **`model.py`**  
  Définit la structure des données et les fonctions associées pour manipuler ces données. Il contient également la logique métier de l'application.

- **`database.py`**  
  Gère la lecture et l'écriture des données dans le fichier `data.json`. Il s'assure que les données sont correctement formatées et stockées.

- **`utils.py`**  
  Contient des fonctions utilitaires ou des outils réutilisables pour le projet.  
  **Exemple de fonctions :**
  - `def validate_input(data):` : Valide les données saisies par l'utilisateur.
  - `def format_output(result):` : Formate les résultats pour l'affichage.

### 2. **Dossier `tests`**
Ce dossier contient tous les tests unitaires pour vérifier le bon fonctionnement du projet.

- **`test_main.py`**  
  Teste les fonctions définies dans `main.py`.  
  **Exemple de tests :**
  - Vérification des résultats des calculs.
  - Gestion des cas limites.

- **`test_gui.py`**  
  Teste les interactions de l'interface graphique.  
  **Exemple de tests :**
  - Vérification que les boutons déclenchent les bonnes actions.
  - Validation des données saisies par l'utilisateur.

- **`test_controller.py`**  
  Teste les fonctions définies dans `controller.py`. Vérifie que les interactions entre la vue et le modèle se déroulent comme prévu.

- **`test_model.py`**  
  Teste les fonctions de manipulation des données définies dans `model.py`. Assure que la logique métier est correctement implémentée.

- **`test_database.py`**  
  Teste les fonctions de lecture et d'écriture dans `data.json` définies dans `database.py`. Vérifie l'intégrité et le format des données.

### 3. **`requirements.txt`**
Ce fichier contient toutes les dépendances nécessaires pour exécuter le projet.  
**Exemple :**

### 4. **`README.md`**
Ce fichier (le fichier actuel) contient une description complète du projet, y compris sa structure, ses fonctionnalités et les instructions pour l'installation et l'exécution.

### 5. **`.gitignore`**
Ce fichier est utilisé pour ignorer certains fichiers ou dossiers dans Git.

---

## **Contributeurs**

- **CEREN MUHAMMED ET SYLLA DAOUDA**  - [EngS1] (https://github.com/EngS1)
