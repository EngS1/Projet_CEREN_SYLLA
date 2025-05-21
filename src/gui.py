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
    afficher_salles_disponibles_pour_creneau,
    afficher_reservations_client,
    charger_donnees,
    sauvegarder_donnees,
    verifier_email,
)
import json


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
        ttk.Label(frame, text="Prénom", background="#f0f8ff").pack(pady=5)
        entry_prenom = ttk.Entry(frame, width=40)
        entry_prenom.pack(pady=5)
        ttk.Label(frame, text="Email", background="#f0f8ff").pack(pady=5)
        entry_email = ttk.Entry(frame, width=40)
        entry_email.pack(pady=5)

        def valider_ajout_client():
            """Valide les entrées et ajoute un client."""
            nom = entry_nom.get().strip()
            prenom = entry_prenom.get().strip()
            email = entry_email.get().strip()
            est_valide, _ = verifier_email(email)
            if not est_valide:
                messagebox.showerror("Erreur", "Email invalide.")
                return
            if not nom or not email:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return

            # Ajout du client
            client = ajouter_client(nom, prenom, email)
            messagebox.showinfo(
                "Succès",
                f"Client ajouté avec succès :\nID: {client['id']}\nNom: {client['nom']}\nPrénom: {client['prenom']}\nEmail: {client['email']}",
            )
            sauvegarder_donnees(fichier_donnees)

        # Boutons Annuler et Valider
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=afficher_boutons_principaux,
            style="Secondary.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Valider",
            command=valider_ajout_client,
            style="Accent.TButton",
            width=15,
        ).pack(side=tk.RIGHT, padx=10)

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

        # Champ pour le nom de la salle (utilisé comme ID)
        ttk.Label(frame, text="Nom de la salle (unique)", background="#f0f8ff").pack(
            pady=5
        )
        entry_nom_salle = ttk.Entry(frame, width=40)
        entry_nom_salle.pack(pady=5)
        error_nom_salle = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_nom_salle.pack()

        # Menu déroulant pour le type de salle
        ttk.Label(frame, text="Type de salle", background="#f0f8ff").pack(pady=5)
        type_salle_var = tk.StringVar()
        type_salle_menu = ttk.Combobox(
            frame, textvariable=type_salle_var, state="readonly", width=37
        )
        type_salle_menu["values"] = ["Standard", "Conférence", "Informatique"]
        type_salle_menu.pack(pady=5)
        error_type_salle = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_type_salle.pack()

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
                capacite_var.set(min(12, capacite_var.get() + 1))

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

        error_capacite = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_capacite.pack()

        def valider_salle():
            """Valide les entrées et ajoute une salle."""
            nom_salle = entry_nom_salle.get().strip()  # Utilisé comme ID et nom
            type_salle = type_salle_var.get()
            capacite = capacite_var.get()

            # Réinitialiser les messages d'erreur
            error_nom_salle.config(text="")
            error_type_salle.config(text="")
            error_capacite.config(text="")

            # Vérification des champs
            erreurs = False
            if not nom_salle:
                error_nom_salle.config(text="Veuillez entrer un nom de salle.")
                erreurs = True
            if not type_salle:
                error_type_salle.config(text="Veuillez sélectionner un type de salle.")
                erreurs = True
            if capacite <= 0:
                error_capacite.config(text="La capacité doit être supérieure à 0.")
                erreurs = True

            # Limitation de la capacité en fonction du type de salle
            if type_salle == "Standard" or type_salle == "Informatique":
                if capacite > 4:
                    error_capacite.config(
                        text="La capacité maximale pour une salle Standard ou Informatique est de 4 personnes."
                    )
                    erreurs = True
            elif type_salle == "Conférence":
                if capacite > 12:
                    error_capacite.config(
                        text="La capacité maximale pour une salle de Conférence est de 12 personnes."
                    )
                    erreurs = True

            if erreurs:
                return

            # Vérification de l'unicité du nom de la salle
            salles_existantes = afficher_salles_disponibles()
            if any(salle["id"] == nom_salle for salle in salles_existantes):
                error_nom_salle.config(
                    text=f"Le nom de la salle '{nom_salle}' existe déjà. Veuillez en choisir un autre."
                )
                return

            # Ajout de la salle (ID et nom sont identiques)
            salle = ajouter_salle(nom_salle, type_salle, capacite)
            messagebox.showinfo(
                "Succès",
                f"Salle ajoutée avec succès :\nNom: {salle['id']}\nType: {salle['type']}\nCapacité: {salle['capacite']}",
            )
            sauvegarder_donnees(fichier_donnees)
            afficher_boutons_principaux()

        # Boutons Annuler et Valider
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=afficher_boutons_principaux,
            style="Secondary.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Valider",
            command=valider_salle,
            style="Accent.TButton",
            width=15,
        ).pack(side=tk.RIGHT, padx=10)

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
            width=35,  # Augmenté de 30 à 35
            style="Accent.TButton",
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouvelle salle",
            command=afficher_formulaire_salle,
            width=35,  # Augmenté de 30 à 35
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
    ttk.Label(frame, text="Date de début", background="#f0f8ff").pack(pady=5)
    entry_date_debut = ttk.Entry(frame, width=40)
    entry_date_debut.pack(pady=5)
    error_date_debut = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_date_debut.pack()

    def ouvrir_calendrier_debut():
        """Ouvre un calendrier pour sélectionner la date de début."""
        top = tk.Toplevel(root)
        top.title("Sélectionner la date de début")
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def valider_date():
            entry_date_debut.delete(0, tk.END)
            entry_date_debut.insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Valider", command=valider_date).pack(pady=10)

    ttk.Button(
        frame,
        text="📅 Choisir",
        command=ouvrir_calendrier_debut,
        width=20,  # Ajusté pour plus de lisibilité
        style="Accent.TButton",
    ).pack(pady=5)

    # Sélection de la date de fin
    ttk.Label(frame, text="Date de fin", background="#f0f8ff").pack(pady=5)
    entry_date_fin = ttk.Entry(frame, width=40)
    entry_date_fin.pack(pady=5)
    error_date_fin = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_date_fin.pack()

    def ouvrir_calendrier_fin():
        """Ouvre un calendrier pour sélectionner la date de fin."""
        top = tk.Toplevel(root)
        top.title("Sélectionner la date de fin")
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def valider_date():
            entry_date_fin.delete(0, tk.END)
            entry_date_fin.insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Valider", command=valider_date).pack(pady=10)

    ttk.Button(
        frame,
        text="📅 Choisir",
        command=ouvrir_calendrier_fin,
        width=20,  # Ajusté pour plus de lisibilité
        style="Accent.TButton",
    ).pack(pady=5)

    # Sélection de l'heure de début
    ttk.Label(frame, text="Heure de début (HH:MM)", background="#f0f8ff").pack(pady=5)
    entry_heure_debut = ttk.Entry(frame, width=40)
    entry_heure_debut.pack(pady=5)
    error_heure_debut = ttk.Label(
        frame, text="", foreground="red", background="#f0f8ff"
    )
    error_heure_debut.pack()

    # Sélection de l'heure de fin
    ttk.Label(frame, text="Heure de fin (HH:MM)", background="#f0f8ff").pack(pady=5)
    entry_heure_fin = ttk.Entry(frame, width=40)
    entry_heure_fin.pack(pady=5)
    error_heure_fin = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_heure_fin.pack()

    # Liste des salles disponibles (menu déroulant)
    ttk.Label(frame, text="Salles disponibles", background="#f0f8ff").pack(pady=10)
    salle_var = tk.StringVar()
    salle_menu = ttk.Combobox(frame, textvariable=salle_var, state="readonly", width=40)
    salle_menu.pack(pady=5)
    error_salle = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_salle.pack()

    def charger_salles_disponibles():
        """Charge les salles disponibles pour les créneaux choisis."""
        date_debut = entry_date_debut.get().strip()
        date_fin = entry_date_fin.get().strip()
        heure_debut = entry_heure_debut.get().strip()
        heure_fin = entry_heure_fin.get().strip()

        # Réinitialiser les messages d'erreur
        error_date_debut.config(text="")
        error_date_fin.config(text="")
        error_heure_debut.config(text="")
        error_heure_fin.config(text="")
        error_salle.config(text="")

        # Vérification des champs
        erreurs = False
        if not date_debut:
            error_date_debut.config(text="Veuillez sélectionner une date de début.")
            erreurs = True
        if not date_fin:
            error_date_fin.config(text="Veuillez sélectionner une date de fin.")
            erreurs = True
        if not heure_debut:
            error_heure_debut.config(text="Veuillez entrer une heure de début.")
            erreurs = True
        if not heure_fin:
            error_heure_fin.config(text="Veuillez entrer une heure de fin.")
            erreurs = True

        if erreurs:
            return

        # Validation des dates
        try:
            date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d").date()
            date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d").date()
            if date_debut_obj > date_fin_obj:
                error_date_fin.config(
                    text="La date de fin doit être égale ou postérieure à la date de début."
                )
                return
        except ValueError:
            error_date_debut.config(text="Format de date invalide (YYYY-MM-DD).")
            return

        # Validation des heures
        try:
            heure_debut_obj = datetime.strptime(heure_debut, "%H:%M")
            heure_fin_obj = datetime.strptime(heure_fin, "%H:%M")
            if heure_debut_obj >= heure_fin_obj:
                error_heure_fin.config(
                    text="L'heure de fin doit être supérieure à l'heure de début."
                )
                return
        except ValueError:
            error_heure_debut.config(text="Format d'heure invalide (HH:MM).")
            return

        # Charger les salles disponibles
        salles = afficher_salles_disponibles_pour_creneau(date_debut, date_fin)
        salle_menu["values"] = [
            f"{salle['id']} - {salle['type']} (Capacité: {salle['capacite']})"
            for salle in salles
        ]


    ttk.Button(
        frame,
        text="Charger les salles",
        command=charger_salles_disponibles,
        width=25,  # Augmenté pour plus de lisibilité
        style="Accent.TButton",
    ).pack(pady=10)

    # Boutons Valider et Annuler
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20)

    ttk.Button(
        button_frame,
        text="Annuler",
        command=lambda: afficher_section(section_accueil),
        style="Secondary.TButton",
        width=20,  # Augmenté pour plus de lisibilité
    ).pack(side=tk.LEFT, padx=10)

    ttk.Button(
        button_frame,
        text="Valider",
        command=lambda: print("Réservation validée"),
        style="Accent.TButton",
        width=20,  # Augmenté pour plus de lisibilité
    ).pack(side=tk.RIGHT, padx=10)

    return frame


def creer_section_afficher():
    """Crée la section Afficher."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Afficher les Informations",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=20)

    # Boutons centraux
    button_frame = ttk.Frame(frame, style="TFrame")
    button_frame.pack(pady=50)

    # Bouton pour afficher la liste des salles
    ttk.Button(
        button_frame,
        text="Afficher liste des salles",
        command=afficher_liste_salles,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    # Bouton pour afficher la liste des clients
    ttk.Button(
        button_frame,
        text="Afficher liste des clients",
        command=afficher_liste_clients,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    # Bouton pour afficher les salles disponibles pour un créneau
    ttk.Button(
        button_frame,
        text="Afficher les salles disponibles pour un créneau",
        command=afficher_salles_pour_creneau,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    # Bouton pour afficher les réservations pour un client
    ttk.Button(
        button_frame,
        text="Afficher les réservations pour un client",
        command=afficher_reservations_client,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    return frame


def afficher_salles_pour_creneau():
    """Affiche les salles disponibles pour un créneau donné."""
    top = tk.Toplevel(root)
    top.title("Salles disponibles pour un créneau")
    top.geometry("400x300")

    ttk.Label(top, text="Date de début (YYYY-MM-DD):").pack(pady=5)
    entry_date_debut = ttk.Entry(top, width=30)
    entry_date_debut.pack(pady=5)

    ttk.Label(top, text="Date de fin (YYYY-MM-DD):").pack(pady=5)
    entry_date_fin = ttk.Entry(top, width=30)
    entry_date_fin.pack(pady=5)

    ttk.Label(top, text="Heure de début (HH:MM):").pack(pady=5)
    entry_heure_debut = ttk.Entry(top, width=30)
    entry_heure_debut.pack(pady=5)

    ttk.Label(top, text="Heure de fin (HH:MM):").pack(pady=5)
    entry_heure_fin = ttk.Entry(top, width=30)
    entry_heure_fin.pack(pady=5)

    def rechercher_salles():
        date_debut = entry_date_debut.get().strip()
        date_fin = entry_date_fin.get().strip()
        heure_debut = entry_heure_debut.get().strip()
        heure_fin = entry_heure_fin.get().strip()

        try:
            salles = afficher_salles_disponibles_pour_creneau(date_debut, date_fin)
            if not salles:
                messagebox.showinfo(
                    "Résultat", "Aucune salle disponible pour ce créneau."
                )
                return

            texte = "\n".join(
                [
                    f"Nom: {salle['id']}, Type: {salle['type']}, Capacité: {salle['capacite']}"
                    for salle in salles
                ]
            )
            messagebox.showinfo("Salles disponibles", texte)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    ttk.Button(top, text="Rechercher", command=rechercher_salles).pack(pady=10)


def afficher_liste_salles():
    """Affiche la liste des salles dans une fenêtre popup."""
    salles = afficher_salles_disponibles()
    if not salles:
        messagebox.showinfo("Information", "Aucune salle disponible.")
        return

    texte = "\n".join(
        [
            f"Nom: {salle['id']}, Type: {salle['type']}, Capacité: {salle['capacite']}"
            for salle in salles
        ]
    )
    messagebox.showinfo("Liste des salles", texte)


def afficher_liste_clients():
    """Affiche la liste des clients dans une fenêtre popup."""
    clients = afficher_clients()
    if not clients:
        messagebox.showinfo("Information", "Aucun client enregistré.")
        return

    texte = "\n".join(
        [
            f"ID: {client['id']}, Nom: {client['nom']}, Email: {client['email']}"
            for client in clients
        ]
    )
    messagebox.showinfo("Liste des clients", texte)


def afficher_reservations_client():
    """Affiche les réservations pour un client donné."""
    top = tk.Toplevel(root)
    top.title("Réservations pour un client")
    top.geometry("400x200")

    ttk.Label(top, text="ID du client:").pack(pady=5)
    entry_client_id = ttk.Entry(top, width=30)
    entry_client_id.pack(pady=5)

    def rechercher_reservations():
        client_id = entry_client_id.get().strip()
        if not client_id:
            messagebox.showerror("Erreur", "Veuillez entrer un ID de client.")
            return

        try:
            reservations = afficher_reservations_client(client_id)
            if not reservations:
                messagebox.showinfo(
                    "Résultat", "Aucune réservation trouvée pour ce client."
                )
                return

            texte = "\n".join(
                [
                    f"Date: {res['date']}, Heure: {res['heure_debut']} - {res['heure_fin']}, Salle: {res['salle_id']}"
                    for res in reservations
                ]
            )
            messagebox.showinfo("Réservations", texte)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    ttk.Button(top, text="Rechercher", command=rechercher_reservations).pack(pady=10)


def menu_principal():
    """Fenêtre principale avec les sections dynamiques."""
    global root
    global section_ajouter, section_reserver, section_afficher, section_accueil

    root = tk.Tk()
    root.title("MeetingPro - Accueil")
    root.geometry("800x700")
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
