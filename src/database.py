from utils import charger_donnees, sauvegarder_donnees

FICHIER_BDD = "data/database.json"

def lire_bdd():
    return charger_donnees(FICHIER_BDD)

def ecrire_bdd(donnees):
    sauvegarder_donnees(FICHIER_BDD, donnees)