import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from main import (
    ajouter_client,
    ajouter_salle,
    afficher_salles_disponibles,
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
    frame = ttk.Frame(root)

    def afficher_formulaire_client():
        """Affiche le formulaire pour ajouter un client."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(frame, text="Ajouter un Client", font=("Helvetica", 14, "bold")).pack(
            pady=10
        )
        ttk.Label(frame, text="Nom").pack(pady=5)
        entry_nom = ttk.Entry(frame, width=40)
        entry_nom.pack(pady=5)

        ttk.Label(frame, text="Prénom").pack(pady=5)
        entry_nom = ttk.Entry(frame, width=40)
        entry_nom.pack(pady=5)

        ttk.Label(frame, text="Email").pack(pady=5)
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

        ttk.Button(frame, text="Confirmer", command=confirmer_client).pack(pady=10)
        ttk.Button(frame, text="Retour", command=afficher_boutons_principaux).pack(
            pady=5
        )

    def afficher_formulaire_salle():
        """Affiche le formulaire pour ajouter une salle."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(frame, text="Ajouter une Salle", font=("Helvetica", 14, "bold")).pack(
            pady=10
        )
        ttk.Label(frame, text="Nom de la salle").pack(pady=5)
        entry_nom_salle = ttk.Entry(frame, width=40)
        entry_nom_salle.pack(pady=5)
        ttk.Label(
            frame, text="Type de salle (standard, conférence, informatique)"
        ).pack(pady=5)
        entry_type = ttk.Entry(frame, width=40)
        entry_type.pack(pady=5)
        ttk.Label(frame, text="Capacité").pack(pady=5)
        entry_capacite = ttk.Entry(frame, width=40)
        entry_capacite.pack(pady=5)

        def confirmer_salle():
            """Valide les entrées et ajoute une salle."""
            nom = entry_nom_salle.get().strip()
            type_salle = entry_type.get().strip()
            capacite = entry_capacite.get().strip()

            if not nom or not type_salle or not capacite.isdigit():
                messagebox.showerror(
                    "Erreur", "Veuillez remplir tous les champs correctement."
                )
                return

            # Ajout de la salle
            salle = ajouter_salle(nom, type_salle, int(capacite))
            messagebox.showinfo(
                "Succès",
                f"Salle ajoutée avec succès :\nNom: {salle['nom']}\nType: {salle['type']}\nCapacité: {salle['capacite']}",
            )
            sauvegarder_donnees(fichier_donnees)

        ttk.Button(frame, text="Confirmer", command=confirmer_salle).pack(pady=10)
        ttk.Button(frame, text="Retour", command=afficher_boutons_principaux).pack(
            pady=5
        )

    def afficher_boutons_principaux():
        """Affiche les boutons principaux de la section Ajouter."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(frame, text="Ajouter", font=("Helvetica", 14, "bold")).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouveau client",
            command=afficher_formulaire_client,
            width=30,
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouvelle salle",
            command=afficher_formulaire_salle,
            width=30,
        ).pack(pady=10)

    afficher_boutons_principaux()
    return frame


def creer_section_reserver():
    """Crée la section Réserver."""
    frame = ttk.Frame(root)

    ttk.Label(frame, text="Réserver une Salle", font=("Helvetica", 14, "bold")).pack(
        pady=10
    )
    ttk.Label(frame, text="Cette section est en cours de développement.").pack(pady=20)

    return frame


def creer_section_afficher():
    """Crée la section Afficher."""
    frame = ttk.Frame(root)

    ttk.Label(frame, text="Salles Disponibles", font=("Helvetica", 14, "bold")).pack(
        pady=10
    )
    salles = afficher_salles_disponibles()
    for salle in salles:
        ttk.Label(
            frame,
            text=f"Nom: {salle['nom']}, Type: {salle['type']}, Capacité: {salle['capacite']}",
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
    section_accueil = ttk.Frame(root)
    ttk.Label(
        section_accueil, text="Bienvenue sur MeetingPro", font=("Helvetica", 20, "bold")
    ).pack(pady=20)

    # Boutons centraux
    button_frame = ttk.Frame(section_accueil)
    button_frame.pack(pady=50)
    ttk.Button(
        button_frame,
        text="Ajouter",
        command=lambda: afficher_section(section_ajouter),
        width=20,
    ).pack(pady=10)
    ttk.Button(
        button_frame,
        text="Réserver",
        command=lambda: afficher_section(section_reserver),
        width=20,
    ).pack(pady=10)
    ttk.Button(
        button_frame,
        text="Afficher",
        command=lambda: afficher_section(section_afficher),
        width=20,
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
