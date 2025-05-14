# Projet_CEREN_SYLLA

## Description
Le projet **CEREN_SYLLA** est une application Python qui combine une interface graphique (Tkinter) et une logique backend pour résoudre un problème spécifique ou fournir une fonctionnalité particulière. Ce projet est conçu pour être modulaire, testable et facile à maintenir.

---

## Structure du Projet

Voici la structure détaillée du projet :

```
Projet_CEREN_SYLLA
├── src
│   ├── main.py          # Contient la logique principale du projet
│   ├── gui.py           # Interface graphique développée avec Tkinter
│   ├── utils.py         # Fonctions utilitaires réutilisables
│   └── __init__.py      # Permet de traiter le dossier comme un package Python
├── tests
│   ├── test_main.py     # Tests unitaires pour les fonctions de main.py
│   ├── test_gui.py      # Tests unitaires pour l'interface graphique
│   ├── test_utils.py    # Tests unitaires pour les fonctions utilitaires
│   └── __init__.py      # Permet de traiter le dossier comme un package Python
├── requirements.txt      # Liste des dépendances nécessaires
├── README.md             # Documentation complète du projet
└── .gitignore            # Fichier pour ignorer certains fichiers/dossiers dans Git
```

### Détails des fichiers et dossiers

#### 1. **Dossier `src`**
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

- **`utils.py`**  
  Contient des fonctions utilitaires ou des outils réutilisables pour le projet.  
  **Exemple de fonctions :**
  - `def validate_input(data):` : Valide les données saisies par l'utilisateur.
  - `def format_output(result):` : Formate les résultats pour l'affichage.

#### 2. **Dossier `tests`**
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

- **`test_utils.py`**  
  Teste les fonctions utilitaires définies dans `utils.py`.  
  **Exemple de tests :**
  - Vérification de la validation des données.
  - Vérification du formatage des résultats.

#### 3. **`requirements.txt`**
Ce fichier contient toutes les dépendances nécessaires pour exécuter le projet.  
**Exemple :**

#### 4. **`README.md`**
Ce fichier (le fichier actuel) contient une description complète du projet, y compris sa structure, ses fonctionnalités et les instructions pour l'installation et l'exécution.

#### 5. **`.gitignore`**
Ce fichier est utilisé pour ignorer certains fichiers ou dossiers dans Git.

---

## Fonctionnalités

1. **Interface Graphique (Tkinter)**  
   - Affichage d'une interface utilisateur intuitive.
   - Interaction avec l'utilisateur via des boutons, des champs de saisie et des étiquettes.
   - Communication avec le backend pour afficher les résultats.

2. **Logique Backend**  
   - Traitement des données saisies par l'utilisateur.
   - Calculs ou traitements spécifiques au projet.
   - Retour des résultats à l'interface graphique.

3. **Tests Unitaires**  
   - Vérification de la validité des fonctions backend.
   - Tests des interactions de l'interface graphique.
   - Validation des fonctions utilitaires.

---

