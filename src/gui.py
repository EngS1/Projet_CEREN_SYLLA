import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from main import (
    ajouter_client,
    afficher_salles_disponibles,
    afficher_clients,
    afficher_salles_disponibles_pour_creneau,
    charger_donnees,
    sauvegarder_donnees,
)
import json


# Charger les données au démarrage
fichier_donnees = "data.json"
charger_donnees(fichier_donnees)


def ajouter_salle(nom_salle, type_salle, capacite):
    """Ajoute une salle dans la base de données."""
    data = charger_donnees()  # Appel sans argument

    # Vérification de l'unicité du nom de la salle
    if any(salle["id"] == nom_salle for salle in data["salles"]):
        raise ValueError(f"Le nom de la salle '{nom_salle}' existe déjà.")

    nouvelle_salle = {
        "id": nom_salle,  # L'ID est identique au nom
        "nom": nom_salle,
        "type": type_salle,
        "capacite": capacite,
    }
    data["salles"].append(nouvelle_salle)
    sauvegarder_donnees(data)  # Appel sans argument
    return nouvelle_salle


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

        # Champ pour le nom
        ttk.Label(frame, text="Nom", background="#f0f8ff").pack(pady=5)
        entry_nom = ttk.Entry(frame, width=40)
        entry_nom.pack(pady=5)
        error_nom = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
        error_nom.pack()

        # Champ pour le prénom
        ttk.Label(frame, text="Prénom", background="#f0f8ff").pack(pady=5)
        entry_prenom = ttk.Entry(frame, width=40)
        entry_prenom.pack(pady=5)
        error_prenom = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
        error_prenom.pack()

        # Champ pour l'email
        ttk.Label(frame, text="Email", background="#f0f8ff").pack(pady=5)
        entry_email = ttk.Entry(frame, width=40)
        entry_email.pack(pady=5)
        error_email = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
        error_email.pack()

        def valider_client():
            """Valide les entrées et ajoute un client."""
            nom = entry_nom.get().strip()
            prenom = entry_prenom.get().strip()
            email = entry_email.get().strip()

            # Réinitialiser les messages d'erreur
            error_nom.config(text="")
            error_prenom.config(text="")
            error_email.config(text="")

            # Validation des champs
            erreurs = False
            if not nom:
                error_nom.config(text="Erreur : Veuillez entrer un nom.")
                erreurs = True
            if not prenom:
                error_prenom.config(text="Erreur : Veuillez entrer un prénom.")
                erreurs = True
            if not email or "@" not in email or "." not in email:
                error_email.config(text="Erreur : Entrez une adresse email correcte.")
                erreurs = True

            if erreurs:
                return

            # Ajout du client
            client = ajouter_client(prenom, nom, email)
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
            command=valider_client,
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
            if not nom_salle or not nom_salle.isalnum():
                error_nom_salle.config(
                    text="Erreur : L'identifiant doit être un nom ou un numéro valide."
                )
                erreurs = True
            if not type_salle:
                error_type_salle.config(
                    text="Erreur : Veuillez sélectionner un type de salle."
                )
                erreurs = True
            if capacite <= 0:
                error_capacite.config(
                    text="Erreur : La capacité doit être supérieure à 0."
                )
                erreurs = True

            # Vérification de l'unicité de l'identifiant
            salles_existantes = afficher_salles_disponibles()
            if any(salle["id"] == nom_salle for salle in salles_existantes):
                error_nom_salle.config(
                    text=f"Erreur : L'identifiant '{nom_salle}' existe déjà. Veuillez en choisir un autre."
                )
                erreurs = True

            if erreurs:
                return

            # Ajout de la salle
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

    def afficher_confirmation():
        """Affiche la page de confirmation dans le même écran."""
        # Sauvegarder les valeurs des champs avant de détruire les widgets
        client_nom = client_var.get()
        date_debut = entry_date_debut.get()
        heure_debut = entry_heure_debut.get()
        date_fin = entry_date_fin.get()
        heure_fin = entry_heure_fin.get()

        # Calcul de la durée
        try:
            datetime_debut = datetime.strptime(
                f"{date_debut} {heure_debut}", "%Y-%m-%d %H:%M"
            )
            datetime_fin = datetime.strptime(
                f"{date_fin} {heure_fin}", "%Y-%m-%d %H:%M"
            )
            duree = datetime_fin - datetime_debut
            duree_heures = duree.total_seconds() // 3600
        except Exception:
            duree_heures = "Inconnue"

        # Détruire les widgets existants
        for widget in frame.winfo_children():
            widget.destroy()

        # Afficher les informations de confirmation
        ttk.Label(
            frame,
            text="Réserver une Salle",
            font=("Helvetica", 16, "bold"),
            background="#f0f8ff",
            anchor="center",
        ).pack(pady=10)

        ttk.Label(
            frame,
            text=f"Client: {client_nom}",
            background="#f0f8ff",
            font=("Helvetica", 12),
            anchor="center",
        ).pack(pady=5)
        ttk.Label(
            frame,
            text=f"Début: {date_debut} {heure_debut}",
            background="#f0f8ff",
            font=("Helvetica", 12),
            anchor="center",
        ).pack(pady=5)
        ttk.Label(
            frame,
            text=f"Fin: {date_fin} {heure_fin}",
            background="#f0f8ff",
            font=("Helvetica", 12),
            anchor="center",
        ).pack(pady=5)
        ttk.Label(
            frame,
            text=f"Durée: {duree_heures}h",
            background="#f0f8ff",
            font=("Helvetica", 12),
            anchor="center",
        ).pack(pady=5)

        # Conteneur pour la sélection des salles et types
        frame_salles = ttk.Frame(frame, style="TFrame")
        frame_salles.pack(pady=10, padx=20, fill=tk.X)

        # Texte "Salle disponible" au-dessus de la case
        ttk.Label(frame_salles, text="Salle disponible:", background="#f0f8ff").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2
        )
        salle_disponible_var = tk.StringVar()
        salle_disponible_menu = ttk.Combobox(
            frame_salles,
            textvariable=salle_disponible_var,
            state="readonly",
            width=30,
        )
        salle_disponible_menu.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Texte "Type de salle" au-dessus de la case
        ttk.Label(frame_salles, text="Type de salle:", background="#f0f8ff").grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.W, columnspan=2
        )
        salle_type_var = tk.StringVar()
        salle_type_var.set("Standard")  # Valeur par défaut
        salle_type_menu = ttk.Combobox(
            frame_salles,
            textvariable=salle_type_var,
            state="readonly",
            values=["Standard", "Conférence", "Informatique"],
            width=20,
        )
        salle_type_menu.grid(row=1, column=2, padx=5, pady=5, columnspan=2)

        def mettre_a_jour_salles():
            """Met à jour la liste des salles disponibles en fonction du type sélectionné."""
            type_salle = salle_type_var.get()
            salles = afficher_salles_disponibles_pour_creneau(date_debut, date_fin)
            salles_filtrees = [
                salle["id"] for salle in salles if salle["type"] == type_salle
            ]
            salle_disponible_menu["values"] = salles_filtrees
            if salles_filtrees:
                salle_disponible_var.set(
                    salles_filtrees[0]
                )  # Sélectionner la première salle
            else:
                salle_disponible_var.set("")  # Réinitialiser si aucune salle disponible

        # Mettre à jour les salles disponibles lorsque le type de salle change
        salle_type_menu.bind("<<ComboboxSelected>>", lambda e: mettre_a_jour_salles())

        # Boutons Annuler et Valider rapprochés au centre
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=lambda: afficher_section(
                section_reserver
            ),  # Retour à la première page
            style="Secondary.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=20)

        ttk.Button(
            button_frame,
            text="Valider",
            command=lambda: messagebox.showinfo(
                "Succès",
                f"Réservation confirmée pour la salle {salle_disponible_var.get()} !",
            ),
            style="Accent.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=20)

    ttk.Label(
        frame,
        text="Réserver une Salle",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
        anchor="center",
    ).pack(pady=10)

    # Conteneur pour la date et l'heure de début
    frame_debut = ttk.Frame(frame, style="TFrame")
    frame_debut.pack(pady=10)
    ttk.Label(frame_debut, text="Date de début", background="#f0f8ff").pack(
        anchor="center", pady=5
    )
    entry_date_debut = ttk.Entry(frame_debut, width=30)
    entry_date_debut.pack(pady=5)
    ttk.Label(frame_debut, text="Heure de début (HH:MM)", background="#f0f8ff").pack(
        anchor="center", pady=5
    )
    entry_heure_debut = ttk.Entry(frame_debut, width=30)
    entry_heure_debut.pack(pady=5)
    ttk.Button(
        frame_debut,
        text="📅 Choisir",
        command=lambda: ouvrir_calendrier(entry_date_debut, entry_heure_debut),
        width=15,
        style="Accent.TButton",
    ).pack(pady=10)

    # Conteneur pour la date et l'heure de fin
    frame_fin = ttk.Frame(frame, style="TFrame")
    frame_fin.pack(pady=10)
    ttk.Label(frame_fin, text="Date de fin", background="#f0f8ff").pack(
        anchor="center", pady=5
    )
    entry_date_fin = ttk.Entry(frame_fin, width=30)
    entry_date_fin.pack(pady=5)
    ttk.Label(frame_fin, text="Heure de fin (HH:MM)", background="#f0f8ff").pack(
        anchor="center", pady=5
    )
    entry_heure_fin = ttk.Entry(frame_fin, width=30)
    entry_heure_fin.pack(pady=5)
    ttk.Button(
        frame_fin,
        text="📅 Choisir",
        command=lambda: ouvrir_calendrier(entry_date_fin, entry_heure_fin),
        width=15,
        style="Accent.TButton",
    ).pack(pady=10)

    # Conteneur pour la liste des clients
    frame_client = ttk.Frame(frame, style="TFrame")
    frame_client.pack(pady=10)
    ttk.Label(frame_client, text="Client", background="#f0f8ff").pack(
        anchor="center", pady=5
    )
    client_var = tk.StringVar()
    client_menu = ttk.Combobox(
        frame_client, textvariable=client_var, state="readonly", width=37
    )
    client_menu["values"] = [
        f"{client['id']} - {client['nom']} {client['prenom']}"
        for client in afficher_clients()
    ]
    client_menu.pack(pady=5)

    # Boutons Valider et Annuler
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20)

    ttk.Button(
        button_frame,
        text="Annuler",
        command=lambda: afficher_section(section_accueil),
        style="Secondary.TButton",
        width=15,
    ).pack(side=tk.LEFT, padx=10)

    ttk.Button(
        button_frame,
        text="Valider",
        command=afficher_confirmation,
        style="Accent.TButton",
        width=15,
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


def ouvrir_calendrier(entry_date, entry_time):
    """Ouvre un calendrier pour sélectionner une date, une heure et une minute."""
    top = tk.Toplevel(root)
    top.title("Sélectionner une date et une heure")
    cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20)

    # Sélection de l'heure
    ttk.Label(top, text="Heure (HH):").pack(pady=5)
    spin_heure = ttk.Spinbox(top, from_=0, to=23, width=5, format="%02.0f")
    spin_heure.pack(pady=5)

    # Sélection de la minute
    ttk.Label(top, text="Minute (MM):").pack(pady=5)
    spin_minute = ttk.Spinbox(top, from_=0, to=59, width=5, format="%02.0f")
    spin_minute.pack(pady=5)
    ttk.Label(top, text="Heure (HH):").pack(pady=5)
    spin_heure = ttk.Spinbox(top, from_=0, to=23, width=5, format="%02.0f")
    spin_heure.pack(pady=5)

    # Sélection de la minute
    ttk.Label(top, text="Minute (MM):").pack(pady=5)
    spin_minute = ttk.Spinbox(top, from_=0, to=59, width=5, format="%02.0f")
    spin_minute.pack(pady=5)

    def confirmer_date_heure():
        # Récupérer la date, l'heure et la minute sélectionnées
        date = cal.get_date()
        heure = spin_heure.get()
        minute = spin_minute.get()

        # Mettre à jour les champs d'entrée
        entry_date.delete(0, tk.END)
        entry_date.insert(0, date)

        entry_time.delete(0, tk.END)
        entry_time.insert(0, f"{heure}:{minute}")

        top.destroy()

    ttk.Button(top, text="Confirmer", command=confirmer_date_heure).pack(pady=10)


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
