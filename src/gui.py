import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from main import (
    ajouter_client,
    ajouter_salle,
    afficher_salles_disponibles,
    reserver_salle,
    afficher_reservations_client,
    verifier_disponibilite_salle,
    afficher_salles_disponibles_pour_creneau,
    supprimer_client,
    supprimer_salle,
    charger_donnees,
    sauvegarder_donnees
)

# Charger les données au démarrage
fichier_donnees = "data.json"
charger_donnees(fichier_donnees)

def ajouter_client_gui():
    """Fenêtre pour ajouter un nouveau client."""
    def confirmer():
        """Valide les entrées et ajoute un client."""
        nom = entry_nom.get().strip()
        email = entry_email.get().strip()

        if not nom or not email:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Ajout du client
        client = ajouter_client(nom, email)
        messagebox.showinfo("Succès", f"Client ajouté avec succès :\nID: {client['id']}\nNom: {client['nom']}\nEmail: {client['email']}")
        sauvegarder_donnees(fichier_donnees)  # Sauvegarde des données
        window.destroy()

    # Création de la fenêtre
    window = tk.Toplevel()
    window.title("Ajouter un client")
    window.geometry("400x250")
    window.resizable(False, False)

    # Titre
    ttk.Label(window, text="Ajouter un nouveau client", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Champ pour le nom
    ttk.Label(window, text="Nom").pack(pady=5)
    entry_nom = ttk.Entry(window, width=40)
    entry_nom.pack(pady=5)

    # Champ pour l'email
    ttk.Label(window, text="Email").pack(pady=5)
    entry_email = ttk.Entry(window, width=40)
    entry_email.pack(pady=5)

    # Bouton de confirmation
    ttk.Button(window, text="Confirmer", command=confirmer).pack(pady=15)

    # Bouton pour fermer la fenêtre
    ttk.Button(window, text="Annuler", command=window.destroy).pack(pady=5)

def ajouter_salle_gui():
    def confirmer():
        nom = entry_nom.get()
        type_salle = entry_type.get()
        capacite = entry_capacite.get()
        if nom and type_salle and capacite.isdigit():
            salle = ajouter_salle(nom, type_salle, int(capacite))
            messagebox.showinfo("Succès", f"Salle ajoutée : {salle}")
            sauvegarder_donnees(fichier_donnees)
            window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")

    window = tk.Toplevel()
    window.title("Ajouter une salle")
    tk.Label(window, text="Ajouter une nouvelle salle", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Nom de la salle").pack(pady=5)
    entry_nom = tk.Entry(window, width=30)
    entry_nom.pack(pady=5)
    tk.Label(window, text="Type de salle (standard, conférence, informatique)").pack(pady=5)
    entry_type = tk.Entry(window, width=30)
    entry_type.pack(pady=5)
    tk.Label(window, text="Capacité").pack(pady=5)
    entry_capacite = tk.Entry(window, width=30)
    entry_capacite.pack(pady=5)
    tk.Button(window, text="Confirmer", command=confirmer, bg="green", fg="white").pack(pady=10)

def afficher_salles_reservables_gui():
    salles = afficher_salles_disponibles()
    window = tk.Toplevel()
    window.title("Salles Réservables")
    for salle in salles:
        tk.Label(window, text=f"Nom: {salle['nom']}, Type: {salle['type']}, Capacité: {salle['capacite']}").pack()
    tk.Button(window, text="Fermer", command=window.destroy).pack()

def afficher_reservations_client_gui():
    def rechercher():
        client_id = entry_client_id.get()
        reservations = afficher_reservations_client(client_id)
        if reservations:
            for res in reservations:
                tk.Label(window, text=f"Réservation: Salle {res['salle_id']}, Début: {res['date_debut']}, Fin: {res['date_fin']}").pack()
        else:
            messagebox.showinfo("Info", "Aucune réservation trouvée pour ce client.")

    window = tk.Toplevel()
    window.title("Réservations du Client")
    tk.Label(window, text="Identifiant du client").pack()
    entry_client_id = tk.Entry(window)
    entry_client_id.pack()
    tk.Button(window, text="Rechercher", command=rechercher).pack()

def verifier_disponibilite_salle_gui():
    def verifier():
        salle_id = entry_salle_id.get()
        date_debut = entry_date_debut.get()
        date_fin = entry_date_fin.get()
        disponible = verifier_disponibilite_salle(salle_id, date_debut, date_fin)
        if disponible:
            messagebox.showinfo("Disponible", "La salle est disponible pour ce créneau.")
        else:
            messagebox.showinfo("Indisponible", "La salle n'est pas disponible pour ce créneau.")

    window = tk.Toplevel()
    window.title("Vérifier Disponibilité Salle")
    tk.Label(window, text="Identifiant de la salle").pack()
    entry_salle_id = tk.Entry(window)
    entry_salle_id.pack()
    tk.Label(window, text="Date de début (YYYY-MM-DD HH:MM)").pack()
    entry_date_debut = tk.Entry(window)
    entry_date_debut.pack()
    tk.Label(window, text="Date de fin (YYYY-MM-DD HH:MM)").pack()
    entry_date_fin = tk.Entry(window)
    entry_date_fin.pack()
    tk.Button(window, text="Vérifier", command=verifier).pack()

def reserver_salle_gui():
    def confirmer():
        client_id = entry_client_id.get()
        salle_id = entry_salle_id.get()
        date_debut = entry_date_debut.get()
        date_fin = entry_date_fin.get()
        if client_id and salle_id and date_debut and date_fin:
            reservation = reserver_salle(client_id, salle_id, date_debut, date_fin)
            messagebox.showinfo("Succès", f"Réservation effectuée : {reservation}")
            sauvegarder_donnees(fichier_donnees)
            window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    window = tk.Toplevel()
    window.title("Réserver une Salle")
    tk.Label(window, text="Identifiant du client").pack()
    entry_client_id = tk.Entry(window)
    entry_client_id.pack()
    tk.Label(window, text="Identifiant de la salle").pack()
    entry_salle_id = tk.Entry(window)
    entry_salle_id.pack()
    tk.Label(window, text="Date de début (YYYY-MM-DD HH:MM)").pack()
    entry_date_debut = tk.Entry(window)
    entry_date_debut.pack()
    tk.Label(window, text="Date de fin (YYYY-MM-DD HH:MM)").pack()
    entry_date_fin = tk.Entry(window)
    entry_date_fin.pack()
    tk.Button(window, text="Confirmer", command=confirmer).pack()

def afficher_salles_disponibles_pour_creneau_gui():
    def rechercher():
        date_debut = entry_date_debut.get()
        date_fin = entry_date_fin.get()
        salles = afficher_salles_disponibles_pour_creneau(date_debut, date_fin)
        if salles:
            for salle in salles:
                tk.Label(window, text=f"Nom: {salle['nom']}, Type: {salle['type']}, Capacité: {salle['capacite']}").pack()
        else:
            messagebox.showinfo("Info", "Aucune salle disponible pour ce créneau.")

    window = tk.Toplevel()
    window.title("Salles disponibles pour un créneau")
    tk.Label(window, text="Date de début (YYYY-MM-DDTHH:MM:SS)").pack(pady=5)
    entry_date_debut = tk.Entry(window, width=30)
    entry_date_debut.pack(pady=5)
    tk.Label(window, text="Date de fin (YYYY-MM-DDTHH:MM:SS)").pack(pady=5)
    entry_date_fin = tk.Entry(window, width=30)
    entry_date_fin.pack(pady=5)
    tk.Button(window, text="Rechercher", command=rechercher, bg="blue", fg="white").pack(pady=10)

def supprimer_client_gui():
    def confirmer():
        client_id = entry_client_id.get()
        if client_id:
            message = supprimer_client(client_id)
            messagebox.showinfo("Succès", message)
            sauvegarder_donnees(fichier_donnees)
            window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un identifiant de client valide.")

    window = tk.Toplevel()
    window.title("Supprimer un client")
    tk.Label(window, text="Identifiant du client").pack(pady=5)
    entry_client_id = tk.Entry(window, width=30)
    entry_client_id.pack(pady=5)
    tk.Button(window, text="Confirmer", command=confirmer, bg="red", fg="white").pack(pady=10)

def supprimer_salle_gui():
    def confirmer():
        salle_id = entry_salle_id.get()
        if salle_id:
            message = supprimer_salle(salle_id)
            messagebox.showinfo("Succès", message)
            sauvegarder_donnees(fichier_donnees)
            window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un identifiant de salle valide.")

    window = tk.Toplevel()
    window.title("Supprimer une salle")
    tk.Label(window, text="Identifiant de la salle").pack(pady=5)
    entry_salle_id = tk.Entry(window, width=30)
    entry_salle_id.pack(pady=5)
    tk.Button(window, text="Confirmer", command=confirmer, bg="red", fg="white").pack(pady=10)

def page_administrateur():
    def retour():
        admin_window.destroy()
        root.deiconify()  # Réaffiche la fenêtre principale

    admin_window = tk.Toplevel()
    admin_window.title("Page Administrateur")
    tk.Label(admin_window, text="Menu Administrateur", font=("Helvetica", 16, "bold")).pack(pady=10)

    tk.Button(admin_window, text="Ajout de nouveau client", command=ajouter_client_gui, width=30).pack(pady=5)
    tk.Button(admin_window, text="Ajout de nouvelle salle", command=ajouter_salle_gui, width=30).pack(pady=5)
    tk.Button(admin_window, text="Afficher salles disponibles pour un créneau", command=afficher_salles_disponibles_pour_creneau_gui, width=30).pack(pady=5)
    tk.Button(admin_window, text="Supprimer un client", command=supprimer_client_gui, width=30).pack(pady=5)
    tk.Button(admin_window, text="Supprimer une salle", command=supprimer_salle_gui, width=30).pack(pady=5)
    tk.Button(admin_window, text="Retour", command=retour, bg="red", fg="white", width=30).pack(pady=10)

def page_client():
    """Fenêtre principale pour les clients."""
    def consulter_reservations():
        """Affiche les réservations du client."""
        afficher_reservations_client_gui()

    def rechercher_salles():
        """Affiche les salles disponibles pour un créneau."""
        afficher_salles_disponibles_pour_creneau_gui()

    def reserver():
        """Permet au client de réserver une salle."""
        reserver_salle_gui()

    # Création de la fenêtre client
    client_window = tk.Toplevel()
    client_window.title("Page Client")
    client_window.geometry("400x300")
    client_window.resizable(False, False)

    # Titre
    tk.Label(client_window, text="Menu Client", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Boutons pour les actions client
    tk.Button(client_window, text="Consulter mes réservations", command=consulter_reservations, width=30).pack(pady=5)
    tk.Button(client_window, text="Rechercher des salles disponibles", command=rechercher_salles, width=30).pack(pady=5)
    tk.Button(client_window, text="Réserver une salle", command=reserver, width=30).pack(pady=5)

    # Bouton pour fermer la fenêtre
    tk.Button(client_window, text="Retour", command=client_window.destroy, bg="red", fg="white", width=30).pack(pady=10)

def menu_principal():
    global root
    root = tk.Tk()
    root.title("MeetingPro - Accueil")
    root.geometry("400x300")

    tk.Label(root, text="Bienvenue sur MeetingPro", font=("Helvetica", 16, "bold")).pack(pady=20)
    tk.Button(root, text="Administrateur", command=lambda: [root.withdraw(), page_administrateur()], width=20).pack(pady=10)
    tk.Button(root, text="Client", command=lambda: [root.withdraw(), page_client()], width=20).pack(pady=10)
    tk.Button(root, text="Quitter", command=root.destroy, bg="red", fg="white", width=20).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    menu_principal()
