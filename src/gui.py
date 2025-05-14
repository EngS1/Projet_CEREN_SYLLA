import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from main import (
    ajouter_client,
    ajouter_salle,
    afficher_salles_disponibles,
    afficher_clients,
    charger_donnees,
    sauvegarder_donnees,
)

# Charger les données au démarrage
fichier_donnees = "data.json"
charger_donnees(fichier_donnees)


def afficher_section(frame):
    """Affiche une section spécifique et cache les autres."""
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Frame):
            widget.pack_forget()
    frame.pack(fill=tk.BOTH, expand=True)


def creer_section_ajouter():
    """Crée la section Ajouter."""
    frame = ttk.Frame(root, style="TFrame")

    def afficher_formulaire_client():
        """Affiche le formulaire pour ajouter un client."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame,
            text="Ajouter un Client",
            font=("Helvetica", 16, "bold"),
            background="#f0f8ff",
        ).pack(pady=10)
        ttk.Label(frame, text="Nom", background="#f0f8ff").pack(pady=5)
        entry_nom = ttk.Entry(frame, width=40)
        entry_nom.pack(pady=5)
        ttk.Label(frame, text="Email", background="#f0f8ff").pack(pady=5)
        entry_email = ttk.Entry(frame, width=40)
        entry_email.pack(pady=5)

        def confirmer_client():
            """Valide les entrées et ajoute un client."""
            nom = entry_nom.get().strip()
            email = entry_email.get().strip()

            if not nom or not email:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return

            # Ajout du client
            client = ajouter_client(nom, email)
            messagebox.showinfo(
                "Succès",
                f"Client ajouté avec succès :\nID: {client['id']}\nNom: {client['nom']}\nEmail: {client['email']}",
            )
            sauvegarder_donnees(fichier_donnees)

        ttk.Button(
            frame, text="Confirmer", command=confirmer_client, style="Accent.TButton"
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Retour",
            command=afficher_boutons_principaux,
            style="Secondary.TButton",
        ).pack(pady=5)

    def afficher_formulaire_salle():
        """Affiche le formulaire pour ajouter une salle."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame,
            text="Ajouter une Salle",
            font=("Helvetica", 16, "bold"),
            background="#f0f8ff",
        ).pack(pady=10)

        # Champ pour l'identifiant de la salle
        ttk.Label(
            frame, text="Identifiant de la salle (unique)", background="#f0f8ff"
        ).pack(pady=5)
        entry_id_salle = ttk.Entry(frame, width=40)
        entry_id_salle.pack(pady=5)

        # Menu déroulant pour le type de salle
        ttk.Label(frame, text="Type de salle", background="#f0f8ff").pack(pady=5)
        type_salle_var = tk.StringVar()
        type_salle_menu = ttk.Combobox(
            frame, textvariable=type_salle_var, state="readonly", width=37
        )
        type_salle_menu["values"] = ["Standard", "Conférence", "Informatique"]
        type_salle_menu.pack(pady=5)

        # Champ pour la capacité (incrémentable)
        ttk.Label(frame, text="Capacité", background="#f0f8ff").pack(pady=5)
        capacite_var = tk.IntVar(value=1)  # Capacité commence à 1
        frame_capacite = ttk.Frame(frame, style="TFrame")
        frame_capacite.pack(pady=5)

        def incrementer_capacite():
            """Incrémente la capacité en fonction du type de salle."""
            type_salle = type_salle_var.get()
            if type_salle == "Standard" or type_salle == "Informatique":
                capacite_var.set(min(4, capacite_var.get() + 1))
            elif type_salle == "Conférence":
                capacite_var.set(min(10, capacite_var.get() + 1))

        def decrementer_capacite():
            """Décrémente la capacité (minimum 1)."""
            capacite_var.set(max(1, capacite_var.get() - 1))

        ttk.Button(frame_capacite, text="-", command=decrementer_capacite).pack(
            side=tk.LEFT
        )
        ttk.Label(
            frame_capacite, textvariable=capacite_var, width=5, anchor="center"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_capacite, text="+", command=incrementer_capacite).pack(
            side=tk.LEFT
        )

        def confirmer_salle():
            """Valide les entrées et ajoute une salle."""
            id_salle = entry_id_salle.get().strip()
            type_salle = type_salle_var.get()
            capacite = capacite_var.get()

            if not id_salle or not type_salle:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return

            # Vérification de l'unicité de l'identifiant
            salles_existantes = afficher_salles_disponibles()
            if any(salle["id"] == id_salle for salle in salles_existantes):
                messagebox.showerror(
                    "Erreur",
                    "L'identifiant de la salle existe déjà. Veuillez en choisir un autre.",
                )
                return

            # Ajout de la salle
            salle = ajouter_salle(id_salle, type_salle, capacite)
            messagebox.showinfo(
                "Succès",
                f"Salle ajoutée avec succès :\nID: {salle['id']}\nType: {salle['type']}\nCapacité: {salle['capacite']}",
            )
            sauvegarder_donnees(fichier_donnees)
            afficher_boutons_principaux()

        # Boutons Valider et Annuler
        ttk.Button(
            frame, text="Valider", command=confirmer_salle, style="Accent.TButton"
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Annuler",
            command=afficher_boutons_principaux,
            style="Secondary.TButton",
        ).pack(pady=5)

    def afficher_boutons_principaux():
        """Affiche les boutons principaux de la section Ajouter."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame, text="Ajouter", font=("Helvetica", 16, "bold"), background="#f0f8ff"
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouveau client",
            command=afficher_formulaire_client,
            width=30,
            style="Accent.TButton",
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouvelle salle",
            command=afficher_formulaire_salle,
            width=30,
            style="Accent.TButton",
        ).pack(pady=10)

    afficher_boutons_principaux()
    return frame


def creer_section_reserver():
    """Crée la section Réserver."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Réserver une Salle",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)

    # Sélection de la date de début
    ttk.Label(frame, text="Date de début de réservation", background="#f0f8ff").pack(
        pady=5
    )
    entry_date_debut = ttk.Entry(frame, width=40)
    entry_date_debut.pack(pady=5)

    def ouvrir_calendrier_debut():
        """Ouvre un calendrier pour sélectionner la date de début."""
        top = tk.Toplevel(root)
        top.title("Sélectionner la date de début")
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def confirmer_date():
            entry_date_debut.delete(0, tk.END)
            entry_date_debut.insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Confirmer", command=confirmer_date).pack(pady=10)

    ttk.Button(frame, text="📅 Choisir", command=ouvrir_calendrier_debut).pack(pady=5)

    # Sélection de la date de fin
    ttk.Label(frame, text="Date de fin de réservation", background="#f0f8ff").pack(
        pady=5
    )
    entry_date_fin = ttk.Entry(frame, width=40)
    entry_date_fin.pack(pady=5)

    def ouvrir_calendrier_fin():
        """Ouvre un calendrier pour sélectionner la date de fin."""
        top = tk.Toplevel(root)
        top.title("Sélectionner la date de fin")
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def confirmer_date():
            entry_date_fin.delete(0, tk.END)
            entry_date_fin.insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Confirmer", command=confirmer_date).pack(pady=10)

    ttk.Button(frame, text="📅 Choisir", command=ouvrir_calendrier_fin).pack(pady=5)

    # Liste des clients enregistrés (menu déroulant)
    ttk.Label(frame, text="Sélectionner un client", background="#f0f8ff").pack(pady=10)
    client_var = tk.StringVar()
    client_menu = ttk.Combobox(
        frame, textvariable=client_var, state="readonly", width=37
    )
    client_menu.pack(pady=5)

    # Charger les clients dans le menu déroulant
    clients = afficher_clients()
    client_menu["values"] = [
        f"{client['id']} - {client['nom']} ({client['email']})" for client in clients
    ]

    def confirmer_reservation():
        """Valide les entrées et effectue la réservation."""
        date_debut = entry_date_debut.get().strip()
        date_fin = entry_date_fin.get().strip()
        client_selection = client_var.get()

        if not client_selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client.")
            return

        if not date_debut or not date_fin:
            messagebox.showerror(
                "Erreur", "Veuillez sélectionner les dates de réservation."
            )
            return

        # Vérification des dates
        try:
            date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
            date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d")
            if date_debut_obj > date_fin_obj:
                messagebox.showerror(
                    "Erreur",
                    "La date de début ne peut pas être supérieure à la date de fin.",
                )
                return
        except ValueError:
            messagebox.showerror(
                "Erreur", "Format de date invalide. Utilisez le format YYYY-MM-DD."
            )
            return

        # Extraire l'ID du client sélectionné
        client_id = client_selection.split(" - ")[0]

        # Effectuer la réservation (fonction à implémenter dans `main.py`)
        messagebox.showinfo(
            "Succès",
            f"Réservation effectuée pour le client ID {client_id} du {date_debut} au {date_fin}.",
        )

    # Boutons Valider et Annuler
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20)
    ttk.Button(
        button_frame,
        text="Valider",
        command=confirmer_reservation,
        style="Accent.TButton",
    ).pack(side=tk.LEFT, padx=10)
    ttk.Button(
        button_frame,
        text="Annuler",
        command=lambda: afficher_section(section_accueil),
        style="Secondary.TButton",
    ).pack(side=tk.LEFT, padx=10)

    return frame


def creer_section_afficher():
    """Crée la section Afficher."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Salles Disponibles",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)
    salles = afficher_salles_disponibles()
    for salle in salles:
        ttk.Label(
            frame,
            text=f"Nom: {salle['nom']}, Type: {salle['type']}, Capacité: {salle['capacite']}",
            background="#f0f8ff",
        ).pack(pady=5)

    return frame


def menu_principal():
    """Fenêtre principale avec les sections dynamiques."""
    global root
    global section_ajouter, section_reserver, section_afficher

    root = tk.Tk()
    root.title("MeetingPro - Accueil")
    root.geometry("600x400")
    root.resizable(False, False)
    root.configure(bg="#f0f8ff")

    # Barre de navigation
    menu_bar = tk.Menu(root)
    menu_bar.add_command(
        label="Accueil", command=lambda: afficher_section(section_accueil)
    )
    menu_bar.add_command(
        label="Ajouter", command=lambda: afficher_section(section_ajouter)
    )
    menu_bar.add_command(
        label="Réserver", command=lambda: afficher_section(section_reserver)
    )
    menu_bar.add_command(
        label="Afficher", command=lambda: afficher_section(section_afficher)
    )
    root.config(menu=menu_bar)

    # Section Accueil
    section_accueil = ttk.Frame(root, style="TFrame")
    ttk.Label(
        section_accueil,
        text="Bienvenue sur MeetingPro",
        font=("Helvetica", 20, "bold"),
        background="#f0f8ff",
    ).pack(pady=20)

    # Boutons centraux
    button_frame = ttk.Frame(section_accueil, style="TFrame")
    button_frame.pack(pady=50)
    ttk.Button(
        button_frame,
        text="Ajouter",
        command=lambda: afficher_section(section_ajouter),
        width=20,
        style="Accent.TButton",
    ).pack(pady=10)
    ttk.Button(
        button_frame,
        text="Réserver",
        command=lambda: afficher_section(section_reserver),
        width=20,
        style="Accent.TButton",
    ).pack(pady=10)
    ttk.Button(
        button_frame,
        text="Afficher",
        command=lambda: afficher_section(section_afficher),
        width=20,
        style="Accent.TButton",
    ).pack(pady=10)

    # Sections dynamiques
    section_ajouter = creer_section_ajouter()
    section_reserver = creer_section_reserver()
    section_afficher = creer_section_afficher()

    # Afficher la section Accueil par défaut
    afficher_section(section_accueil)

    root.mainloop()


if __name__ == "__main__":
    menu_principal()
