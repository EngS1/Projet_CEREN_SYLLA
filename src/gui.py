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
    reserver_salle,
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
                messagebox.showerror(
                    "Erreur", "Veuillez remplir tous les champs.")
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
        ttk.Label(frame, text="Type de salle",
                  background="#f0f8ff").pack(pady=5)
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
                error_type_salle.config(
                    text="Veuillez sélectionner un type de salle.")
                erreurs = True
            if capacite <= 0:
                error_capacite.config(
                    text="La capacité doit être supérieure à 0.")
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


def ouvrir_calendrier(entry, parent_window):
    """Crée une fenêtre de sélection de créneau avec un calendrier et des heures."""
    top = tk.Toplevel(parent_window)
    top.title("Sélection du créneau")
    top.geometry("400x500")

    # Frame principale
    main_frame = ttk.Frame(top, padding=10)
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Calendrier
    ttk.Label(main_frame, text="Sélectionnez la date:").pack(pady=5)
    cal = Calendar(main_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10, fill=tk.X, padx=20)

    # Sélection de l'heure
    ttk.Label(main_frame, text="Sélectionnez l'heure:").pack(pady=5)
    frame_heure = ttk.Frame(main_frame)
    frame_heure.pack(pady=10)

    # Heures (8h-19h)
    ttk.Label(frame_heure, text="Heure:").pack(side=tk.LEFT)
    heures = [f"{h:02d}" for h in range(8, 20)]
    combo_heure = ttk.Combobox(frame_heure, values=heures, width=3)
    combo_heure.pack(side=tk.LEFT, padx=5)

    # Minutes (par créneaux de 15 min)
    ttk.Label(frame_heure, text="Min:").pack(side=tk.LEFT)
    minutes = ["00", "15", "30", "45"]
    combo_min = ttk.Combobox(frame_heure, values=minutes, width=3)
    combo_min.pack(side=tk.LEFT)

    # Bouton Valider
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20, fill=tk.X)

    def valider_creneau():
        """Valide le créneau sélectionné."""
        date = cal.get_date()
        heure = combo_heure.get()
        minute = combo_min.get()

        if heure and minute:
            entry.delete(0, tk.END)
            entry.insert(0, f"{date} {heure}:{minute}:00")
            top.destroy()
        else:
            messagebox.showwarning(
                "Attention", "Veuillez sélectionner une heure complète"
            )

    ttk.Button(btn_frame, text="Valider ce créneau", command=valider_creneau).pack(
        side=tk.BOTTOM
    )


def creer_section_reserver():
    """Crée la section Réserver."""
    frame = ttk.Frame(root, style="TFrame")

    # Efface le contenu du frame à chaque fois
    for widget in frame.winfo_children():
        widget.destroy()

    ttk.Label(
        frame,
        text="Réserver une Salle",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)
    # Sélection de la date de début
    ttk.Label(frame, text="Date de début",
              background="#f0f8ff").pack(pady=5)
    entry_date_debut = ttk.Entry(frame, width=40)
    entry_date_debut.pack(pady=5)
    error_date_debut = ttk.Label(
        frame, text="", foreground="red", background="#f0f8ff")
    error_date_debut.pack()

    def ouvrir_calendrier_debut():
        """Ouvre un calendrier pour sélectionner la date de début."""
        ouvrir_calendrier(entry_date_debut, frame)
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
    error_date_fin = ttk.Label(
        frame, text="", foreground="red", background="#f0f8ff")
    error_date_fin.pack()

    def ouvrir_calendrier_fin():
        """Ouvre un calendrier pour sélectionner la date de fin."""
        ouvrir_calendrier(entry_date_fin, frame)

    ttk.Button(
        frame,
        text="📅 Choisir",
        command=ouvrir_calendrier_fin,
        width=20,  # Ajusté pour plus de lisibilité
        style="Accent.TButton",
    ).pack(pady=5)

    # Liste des clients
    tk.Label(frame, text="Client").pack(pady=5)
    liste_clients = afficher_clients()
    entry_client = ttk.Combobox(
        frame, values=liste_clients, state="readonly", width=40)
    entry_client.set("Sélectionner un client")
    entry_client.pack()
    error_client = ttk.Label(
        frame, text="", foreground="red", background="#f0f8ff")
    error_client.pack()

    # Liste des salles disponibles
    ttk.Label(frame, text="Salles disponibles",
              background="#f0f8ff").pack(pady=10)
    salle_var = tk.StringVar()
    salle_menu = ttk.Combobox(
        frame, textvariable=salle_var, state="readonly", width=40)
    salle_menu.pack(pady=5)
    error_salle = ttk.Label(
        frame, text="", foreground="red", background="#f0f8ff")
    error_salle.pack()

    def charger_salles_disponibles():
        """Charge les salles disponibles pour les créneaux choisis."""
        date_debut_str = entry_date_debut.get().strip()
        date_fin_str = entry_date_fin.get().strip()
        date_debut_obj = datetime.strptime(
            date_debut_str, "%Y-%m-%d %H:%M:%S")

        date_fin_obj = datetime.strptime(date_fin_str, "%Y-%m-%d %H:%M:%S")
        date_debut = date_debut_obj.strftime("%Y-%m-%d")
        date_fin = date_fin_obj.strftime("%Y-%m-%d")
        heure_debut = date_debut_obj.strftime("%H:%M")
        heure_fin = date_fin_obj.strftime("%H:%M")

        # Réinitialiser les messages d'erreur
        error_date_debut.config(text="")
        error_date_fin.config(text="")
        error_salle.config(text="")
        error_client.config(text="")

        # Vérification des champs
        erreurs = False
        if not date_debut:
            error_date_debut.config(
                text="Veuillez sélectionner une date de début.")
            erreurs = True
        if not date_fin:
            error_date_fin.config(
                text="Veuillez sélectionner une date de fin.")
            erreurs = True
        if entry_client.get() == "Sélectionner un client":
            error_client.config(text="Veuillez sélectionner un client.")
            erreurs = True
        if erreurs:
            return

        # Validation des dates
        try:
            if date_debut > date_fin:
                error_date_fin.config(
                    text="La date de fin doit être égale ou postérieure à la date de début."
                )
                return
        except ValueError:
            error_date_debut.config(
                text="Format de date invalide (YYYY-MM-DD).")
            return

        # Validation des heures
        try:
            if heure_debut >= heure_fin:
                error_date_fin.config(
                    text="L'heure de fin doit être supérieure à l'heure de début."
                )
                return
        except ValueError:
            error_date_debut.config(
                text="Format d'heure invalide (HH:MM).")
            return

        # Charger les salles disponibles
        salles = afficher_salles_disponibles_pour_creneau(
            date_debut, date_fin)
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

    def afficher_recapitulatif_reservation(client_nom, date_debut, date_fin, duree, salle_nom, salle_type, salle_capacite):
        # Efface le contenu du frame
        for widget in frame.winfo_children():
            widget.destroy()
        ttk.Label(frame, text="Récapitulatif de la réservation",
                  font=("Helvetica", 14, "bold")).pack(pady=15)
        ttk.Label(frame, text=f"Client : {client_nom}").pack(pady=5)
        ttk.Label(frame, text=f"Date de début : {date_debut}").pack(pady=5)
        ttk.Label(frame, text=f"Date de fin : {date_fin}").pack(pady=5)
        ttk.Label(frame, text=f"Durée : {duree}").pack(pady=5)
        ttk.Label(frame, text=f"Salle : {salle_nom}").pack(pady=5)
        ttk.Label(frame, text=f"Type de salle : {salle_type}").pack(pady=5)
        ttk.Label(frame, text=f"Capacité : {salle_capacite}").pack(pady=5)
        ttk.Button(frame, text="Retour à l'accueil", command=lambda: afficher_section(
            section_accueil)).pack(pady=20)

    def valider_reservation():
        # Réserver la salle
        if salle_menu.get() == "":
            error_salle.config(text="Veuillez sélectionner une salle.")
            return
        reserver_salle(
            entry_client.get(), entry_date_debut.get(), entry_date_fin.get(), salle_var.get()
        )
        # Récupérer les infos pour le récapitulatif
        client_nom = entry_client.get()
        date_debut = entry_date_debut.get()
        date_fin = entry_date_fin.get()
        # Calcul de la durée
        try:
            d1 = datetime.strptime(date_debut, "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(date_fin, "%Y-%m-%d %H:%M:%S")
            duree = str(d2 - d1)
        except Exception:
            duree = "Inconnue"
        # Infos salle
        salle_info = salle_var.get()
        if salle_info:
            # Format attendu : "nom - type (Capacité: X)"
            try:
                salle_nom = salle_info.split(" - ")[0]
                salle_type = salle_info.split(" - ")[1].split(" (")[0]
                salle_capacite = salle_info.split(
                    "Capacité: ")[1].replace(")", "")
            except Exception:
                salle_nom = salle_info
                salle_type = ""
                salle_capacite = ""
        else:
            salle_nom = salle_type = salle_capacite = ""
        # Afficher la fenêtre de récapitulatif
        afficher_recapitulatif_reservation(
            client_nom, date_debut, date_fin, duree, salle_nom, salle_type, salle_capacite)
        messagebox.showinfo("Réserver avec succès",
                            "La réservation est validée")
        sauvegarder_donnees(fichier_donnees)
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
        command=lambda: valider_reservation(),
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
            salles = afficher_salles_disponibles_pour_creneau(
                date_debut, date_fin)
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
            messagebox.showerror(
                "Erreur", f"Erreur lors de la recherche : {e}")

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
            f"ID: {client['id']}, Nom: {client['nom']}, Prénom: {client['prenom']}, Email: {client['email']}"
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
            messagebox.showerror(
                "Erreur", f"Erreur lors de la recherche : {e}")

    ttk.Button(top, text="Rechercher",
               command=rechercher_reservations).pack(pady=10)


def recreer_et_afficher_section_reserver():
    global section_reserver
    section_reserver = creer_section_reserver()
    afficher_section(section_reserver)


def menu_principal():
    """Fenêtre principale avec les sections dynamiques."""
    global root
    global section_ajouter, section_afficher, section_accueil

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
        label="Réserver", command=recreer_et_afficher_section_reserver
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
        command=recreer_et_afficher_section_reserver,
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
   # section_reserver = creer_section_reserver()
    section_afficher = creer_section_afficher()

    # Afficher la section Accueil par défaut
    afficher_section(section_accueil)

    root.mainloop()


if __name__ == "__main__":
    menu_principal()
