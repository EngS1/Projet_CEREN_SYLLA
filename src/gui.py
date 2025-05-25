"""Graphical User Interface for MeetingPro Application."""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from main import (
    add_client,
    add_room,
    display_available_rooms,
    display_clients,
    book_room,
    display_available_rooms_for_niche,
    display_clients_bookings,
    load_data,
    save_data,
    check_email,
)
import json
import logging


"""Logging configuration."""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

logger.info("Application started")


"""Upload data from JSON file."""
file_data = "data.json"
logger.info(f"Loading data from {file_data}")
load_data(file_data)


"""Global variables for sections."""


def display_section(frame) -> None:
    """Show a specific section in the main window."""
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Frame):
            widget.pack_forget()
    frame.pack(fill=tk.BOTH, expand=True)


def create_add_section():
    """Create the section Ajouter."""
    frame = ttk.Frame(root, style="TFrame")

    def display_client_form():
        """Show the form to add a client."""
        logger.info("Displaying client addition form")
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame,
            text="Ajouter un Client",
            font=("Helvetica", 16, "bold"),
            background="#f0f8ff",
        ).pack(pady=10)
        ttk.Label(frame, text="Nom", background="#f0f8ff").pack(pady=5)
        entry_name = ttk.Entry(frame, width=40)
        entry_name.pack(pady=5)
        ttk.Label(frame, text="Prénom", background="#f0f8ff").pack(pady=5)
        entry_surname = ttk.Entry(frame, width=40)
        entry_surname.pack(pady=5)
        ttk.Label(frame, text="Email", background="#f0f8ff").pack(pady=5)
        entry_email = ttk.Entry(frame, width=40)
        entry_email.pack(pady=5)

        def validate_add_client() -> None:
            """Validate the client addition form and add the client."""
            nom = entry_name.get().strip()
            prenom = entry_surname.get().strip()
            email = entry_email.get().strip()
            is_valid, _ = check_email(email)
            if not is_valid:
                logger.warning("Invalid email entered")
                messagebox.showerror("Erreur", "Email invalide.")
                return
            if not nom or not email:
                logger.warning("Missing required fields for client addition")
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return

            """Add the client."""
            client = add_client(nom, prenom, email)
            logger.info(f"Client added successfully: {client}")
            messagebox.showinfo(
                "Succès",
                f"Client ajouté avec succès :\nID: {client['id']}\nNom: {client['nom']}\nPrénom: {client['prenom']}\nEmail: {client['email']}",
            )
            save_data(file_data)

        """Buttons for Cancel and Validate."""
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=display_main_buttons,
            style="Secondary.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Valider",
            command=validate_add_client,
            style="Accent.TButton",
            width=15,
        ).pack(side=tk.RIGHT, padx=10)

    def display_room_form() -> None:
        """Show the form to add a room."""
        logger.info("Displaying room addition form")
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame,
            text="Ajouter une Salle",
            font=("Helvetica", 16, "bold"),
            background="#f0f8ff",
        ).pack(pady=10)

        """Section to add a room."""
        ttk.Label(frame, text="Nom de la salle (unique)", background="#f0f8ff").pack(
            pady=5
        )
        entry_name_room = ttk.Entry(frame, width=40)
        entry_name_room.pack(pady=5)
        error_name_room = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_name_room.pack()

        """Scrollable dropdown for room type."""
        ttk.Label(frame, text="Type de salle", background="#f0f8ff").pack(pady=5)
        type_room_var = tk.StringVar()
        type_room_menu = ttk.Combobox(
            frame, textvariable=type_room_var, state="readonly", width=37
        )
        type_room_menu["values"] = ["Standard", "Conférence", "Informatique"]
        type_room_menu.pack(pady=5)
        error_type_room = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_type_room.pack()

        """Section to set the room capacity."""
        ttk.Label(frame, text="Capacité", background="#f0f8ff").pack(pady=5)
        capacite_var = tk.IntVar(value=1)  # Capacité commence à 1
        frame_capacite = ttk.Frame(frame, style="TFrame")
        frame_capacite.pack(pady=5)

        def incrementer_capacite() -> None:
            """Increase the capacity based on room type."""
            type_room = type_room_var.get()
            if type_room == "Standard" or type_room == "Informatique":
                capacite_var.set(min(4, capacite_var.get() + 1))
            elif type_room == "Conférence":
                capacite_var.set(min(12, capacite_var.get() + 1))

        def decrementer_capacite() -> None:
            """Decrease the capacity, ensuring it doesn't go below 1."""
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

        def validate_room() -> None:
            """Validate the room addition form and add the room."""
            name_room = entry_name_room.get().strip()  # Utilisé comme ID et nom
            type_room = type_room_var.get()
            capacite = capacite_var.get()

            """Reset error messages."""
            error_name_room.config(text="")
            error_type_room.config(text="")
            error_capacite.config(text="")

            logger.info(
                f"Attempting to add room: {name_room} ({type_room}, {capacite})"
            )
            """Validation of the form fields."""
            erreurs = False
            if not name_room:
                error_name_room.config(text="Veuillez entrer un nom de salle.")
                erreurs = True
            if not type_room:
                error_type_room.config(text="Veuillez sélectionner un type de salle.")
                erreurs = True
            if capacite <= 0:
                error_capacite.config(text="La capacité doit être supérieure à 0.")
                erreurs = True

            """Validation of the room type and capacity."""
            if type_room == "Standard" or type_room == "Informatique":
                if capacite > 4:
                    error_capacite.config(
                        text="La capacité maximale pour une salle Standard ou Informatique est de 4 personnes."
                    )
                    erreurs = True
            elif type_room == "Conférence":
                if capacite > 12:
                    error_capacite.config(
                        text="La capacité maximale pour une salle de Conférence est de 12 personnes."
                    )
                    erreurs = True

            if erreurs:
                return

            """Verification of existing room names."""
            existing_rooms = display_available_rooms()
            if any(room["id"] == name_room for room in existing_rooms):
                error_name_room.config(
                    text=f"Le nom de la salle '{name_room}' existe déjà. Veuillez en choisir un autre."
                )
                logger.warning(f"Room name '{name_room}' already exists")
                return

            """Addition of the room."""
            room = add_room(name_room, type_room, capacite)
            logger.info(f"Room added successfully: {room}")
            messagebox.showinfo(
                "Succès",
                f"Salle ajoutée avec succès :\nNom: {room['id']}\nType: {room['type']}\nCapacité: {room['capacite']}",
            )
            save_data(file_data)
            display_main_buttons()

        """Buttons for Cancel and Validate."""
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=display_main_buttons,
            style="Secondary.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Valider",
            command=validate_room,
            style="Accent.TButton",
            width=15,
        ).pack(side=tk.RIGHT, padx=10)

    def display_main_buttons() -> None:
        """Show the main buttons in the 'Add' section."""
        logger.info("Displaying main buttons in 'Add' section")
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame, text="Ajouter", font=("Helvetica", 16, "bold"), background="#f0f8ff"
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouveau client",
            command=display_client_form,
            width=35,  # Augmenté de 30 à 35
            style="Accent.TButton",
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouvelle salle",
            command=display_room_form,
            width=35,  # Augmenté de 30 à 35
            style="Accent.TButton",
        ).pack(pady=10)

    display_main_buttons()
    return frame


def open_calendar(entry, parent_window):
    """Opens a calendar popup to select a date and time."""
    top = tk.Toplevel(parent_window)
    top.title("Sélection du créneau")
    top.geometry("400x500")

    main_frame = ttk.Frame(top, padding=10)
    main_frame.pack(expand=True, fill=tk.BOTH)

    """Label and calendar for date selection."""
    ttk.Label(main_frame, text="Sélectionnez la date:").pack(pady=5)
    cal = Calendar(main_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10, fill=tk.X, padx=20)

    ttk.Label(main_frame, text="Sélectionnez l'heure:").pack(pady=5)
    frame_heure = ttk.Frame(main_frame)
    frame_heure.pack(pady=10)

    """Comboboxes for hour and minute selection."""
    ttk.Label(frame_heure, text="Heure:").pack(side=tk.LEFT)
    heures = [f"{h:02d}" for h in range(8, 20)]
    combo_heure = ttk.Combobox(frame_heure, values=heures, width=3)
    combo_heure.pack(side=tk.LEFT, padx=5)

    """Combobox for minute selection."""
    ttk.Label(frame_heure, text="Min:").pack(side=tk.LEFT)
    minutes = ["00", "15", "30", "45"]
    combo_min = ttk.Combobox(frame_heure, values=minutes, width=3)
    combo_min.pack(side=tk.LEFT)

    """Button frame for validation."""
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20, fill=tk.X)

    def valider_creneau() -> None:
        """Validates the selected date and time, and updates the entry field."""
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


def create_booking_section() -> None:
    """Create the section for reserving a room."""
    frame = ttk.Frame(root, style="TFrame")

    """Clear the frame before adding new widgets."""
    for widget in frame.winfo_children():
        widget.destroy()

    ttk.Label(
        frame,
        text="Réserver une Salle",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)
    """Start date selection."""
    ttk.Label(frame, text="Date de début", background="#f0f8ff").pack(pady=5)
    entry_start_date = ttk.Entry(frame, width=40)
    entry_start_date.pack(pady=5)
    error_start_date = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_start_date.pack()

    def open_calendar_start() -> None:
        """Opens a calendar to select the start date."""
        open_calendar(entry_start_date, frame)

    ttk.Button(
        frame,
        text="📅 Choisir",
        command=open_calendar_start,
        width=20,  # Ajusté pour plus de lisibilité
        style="Accent.TButton",
    ).pack(pady=5)

    """End date selection."""
    ttk.Label(frame, text="Date de fin", background="#f0f8ff").pack(pady=5)
    entry_end_date = ttk.Entry(frame, width=40)
    entry_end_date.pack(pady=5)
    error_end_date = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_end_date.pack()

    def open_calendar_end():
        """Opens a calendar to select the end date."""
        open_calendar(entry_end_date, frame)

    ttk.Button(
        frame,
        text="📅 Choisir",
        command=open_calendar_end,
        width=20,  # Ajusté pour plus de lisibilité
        style="Accent.TButton",
    ).pack(pady=5)

    """Client selection."""
    tk.Label(frame, text="Client").pack(pady=5)
    liste_clients = display_clients()
    entry_client = ttk.Combobox(frame, values=liste_clients, state="readonly", width=40)
    entry_client.set("Sélectionner un client")
    entry_client.pack()
    error_client = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_client.pack()

    """Load clients to the combobox."""
    ttk.Label(frame, text="salles disponibles", background="#f0f8ff").pack(pady=10)
    room_var = tk.StringVar()
    room_menu = ttk.Combobox(frame, textvariable=room_var, state="readonly", width=40)
    room_menu.pack(pady=5)
    error_room = ttk.Label(frame, text="", foreground="red", background="#f0f8ff")
    error_room.pack()

    def load_available_rooms() -> None:
        """Load available rooms based on the selected date and time."""
        start_date_str = entry_start_date.get().strip()
        end_date_str = entry_end_date.get().strip()
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")

        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
        start_date = start_date_obj.strftime("%Y-%m-%d")
        end_date = end_date_obj.strftime("%Y-%m-%d")
        start_hour = start_date_obj.strftime("%H:%M")
        end_hour = end_date_obj.strftime("%H:%M")

        """Reset error messages."""
        error_start_date.config(text="")
        error_end_date.config(text="")
        error_room.config(text="")
        error_client.config(text="")

        """Validation of the form fields."""
        erreurs = False
        if not start_date:
            error_start_date.config(text="Veuillez sélectionner une date de début.")
            erreurs = True
        if not end_date:
            error_end_date.config(text="Veuillez sélectionner une date de fin.")
            erreurs = True
        if entry_client.get() == "Sélectionner un client":
            error_client.config(text="Veuillez sélectionner un client.")
            erreurs = True
        if erreurs:
            return

        """Validation of the dates."""
        try:
            if start_date > end_date:
                error_end_date.config(
                    text="La date de fin doit être égale ou postérieure à la date de début."
                )
                return
        except ValueError:
            error_start_date.config(text="Format de date invalide (YYYY-MM-DD).")
            return

        """Validation of the time."""
        try:
            if start_hour >= end_hour:
                error_end_date.config(
                    text="L'heure de fin doit être supérieure à l'heure de début."
                )
                return
        except ValueError:
            error_start_date.config(text="Format d'heure invalide (HH:MM).")
            return

        """Load available rooms for the selected date and time."""
        rooms = display_available_rooms_for_niche(start_date, end_date)
        room_menu["values"] = [
            f"{room['id']} - {room['type']} (Capacité: {room['capacite']})"
            for room in rooms
        ]

    ttk.Button(
        frame,
        text="Charger les rooms",
        command=load_available_rooms,
        width=25,
        style="Accent.TButton",
    ).pack(pady=10)

    def show_booking_summary(
        cliient_name,
        start_date,
        end_date,
        duration,
        room_name,
        room_type,
        room_capacity,
    ):
        """Display the reservation summary in a new frame."""
        for widget in frame.winfo_children():
            widget.destroy()
        ttk.Label(
            frame,
            text="Récapitulatif de la réservation",
            font=("Helvetica", 14, "bold"),
        ).pack(pady=15)
        ttk.Label(frame, text=f"Client : {cliient_name}").pack(pady=5)
        ttk.Label(frame, text=f"Date de début : {start_date}").pack(pady=5)
        ttk.Label(frame, text=f"Date de fin : {end_date}").pack(pady=5)
        ttk.Label(frame, text=f"Durée : {duration}").pack(pady=5)
        ttk.Label(frame, text=f"Salle : {room_name}").pack(pady=5)
        ttk.Label(frame, text=f"Type de salle : {room_type}").pack(pady=5)
        ttk.Label(frame, text=f"Capacité : {room_capacity}").pack(pady=5)
        ttk.Button(
            frame,
            text="Retour à l'accueil",
            command=lambda: display_section(home_section),
        ).pack(pady=20)

    def validate_booking() -> None:
        """Validate the reservation form and reserve the room."""
        if room_menu.get() == "":
            error_room.config(text="Veuillez sélectionner une room.")
            return
        book_room(
            entry_client.get(),
            entry_start_date.get(),
            entry_end_date.get(),
            room_var.get(),
        )
        """Get the client name, start date, end date, and duration."""
        cliient_name = entry_client.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        """Calculate the duration of the reservation."""
        try:
            d1 = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            duration = str(d2 - d1)
        except Exception:
            duration = "Inconnue"
        """Get the selected room information."""
        room_info = room_var.get()
        if room_info:
            """Parse the room information to extract name, type, and capacity."""
            try:
                room_name = room_info.split(" - ")[0]
                room_type = room_info.split(" - ")[1].split(" (")[0]
                room_capacity = room_info.split("Capacité: ")[1].replace(")", "")
            except Exception:
                room_name = room_info
                room_type = ""
                room_capacity = ""
        else:
            room_name = room_type = room_capacity = ""
        """Display the reservation summary."""
        show_booking_summary(
            cliient_name,
            start_date,
            end_date,
            duration,
            room_name,
            room_type,
            room_capacity,
        )
        messagebox.showinfo("Réserver avec succès", "La réservation est validée")
        save_data(file_data)

    """Buttons for Cancel and Validate."""
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20)

    ttk.Button(
        button_frame,
        text="Annuler",
        command=lambda: display_section(home_section),
        style="Secondary.TButton",
        width=20,
    ).pack(side=tk.LEFT, padx=10)

    ttk.Button(
        button_frame,
        text="Valider",
        command=lambda: validate_booking(),
        style="Accent.TButton",
        width=20,
    ).pack(side=tk.RIGHT, padx=10)

    return frame


def create_display_section() -> ttk.Frame:
    """Create the section for displaying information."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Afficher les Informations",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=20)

    """Button frame for displaying information."""
    button_frame = ttk.Frame(frame, style="TFrame")
    button_frame.pack(pady=50)

    """Button to display the list of rooms."""
    ttk.Button(
        button_frame,
        text="Afficher liste des salles",
        command=display_rooms_lists,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    """Button to display the list of clients."""
    ttk.Button(
        button_frame,
        text="Afficher liste des clients",
        command=display_cliemt_list,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    """Button to display available rooms for a time slot."""
    ttk.Button(
        button_frame,
        text="Afficher les rooms disponibles pour un créneau",
        command=display_rooms_for_niche,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    """Button to display bookings for a client."""
    ttk.Button(
        button_frame,
        text="Afficher les réservations pour un client",
        command=display_clients_bookings_gui,
        width=45,  # Augmenté de 40 à 45
        style="Accent.TButton",
    ).pack(pady=10)

    return frame


def display_rooms_for_niche() -> None:
    """Show a popup to find available rooms for a time slot."""
    top = tk.Toplevel(root)
    top.title("rooms disponibles pour un créneau")
    top.geometry("400x300")

    ttk.Label(top, text="Date de début (YYYY-MM-DD):").pack(pady=5)
    entry_start_date = ttk.Entry(top, width=30)
    entry_start_date.pack(pady=5)

    ttk.Label(top, text="Date de fin (YYYY-MM-DD):").pack(pady=5)
    entry_end_date = ttk.Entry(top, width=30)
    entry_end_date.pack(pady=5)

    ttk.Label(top, text="Heure de début (HH:MM):").pack(pady=5)
    entry_start_hour = ttk.Entry(top, width=30)
    entry_start_hour.pack(pady=5)

    ttk.Label(top, text="Heure de fin (HH:MM):").pack(pady=5)
    entry_end_hour = ttk.Entry(top, width=30)
    entry_end_hour.pack(pady=5)

    def rechercher_rooms() -> None:
        """Search for available rooms based on the provided date and time."""
        start_date = entry_start_date.get().strip()
        end_date = entry_end_date.get().strip()
        start_hour = entry_start_hour.get().strip()
        end_hour = entry_end_hour.get().strip()

        try:
            rooms = display_available_rooms_for_niche(start_date, end_date)
            if not rooms:
                messagebox.showinfo(
                    "Résultat", "Aucune salle disponible pour ce créneau."
                )
                return

            texte = "\n".join(
                [
                    f"Nom: {room['id']}, Type: {room['type']}, Capacité: {room['capacite']}"
                    for room in rooms
                ]
            )
            messagebox.showinfo("rooms disponibles", texte)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    ttk.Button(top, text="Rechercher", command=rechercher_rooms).pack(pady=10)


def display_rooms_lists() -> None:
    """Show the list of available rooms in a popup."""
    rooms = display_available_rooms()
    if not rooms:
        messagebox.showinfo("Information", "Aucune room disponible.")
        return

    texte = "\n".join(
        [
            f"Nom: {room['id']}, Type: {room['type']}, Capacité: {room['capacite']}"
            for room in rooms
        ]
    )
    messagebox.showinfo("Liste des rooms", texte)


def display_cliemt_list() -> None:
    """Show the list of registered clients in a popup."""
    """Display the list of clients in a popup."""
    clients = display_clients()
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


def display_clients_bookings_gui() -> None:
    """Show a popup to search for bookings by client ID."""
    top = tk.Toplevel(root)
    top.title("Réservations pour un client")
    top.geometry("400x200")

    ttk.Label(top, text="ID du client:").pack(pady=5)
    entry_client_id = ttk.Entry(top, width=30)
    entry_client_id.pack(pady=5)

    def rechercher_bookings() -> None:
        client_id = entry_client_id.get().strip()
        if not client_id:
            messagebox.showerror("Erreur", "Veuillez entrer un ID de client.")
            return

        try:
            bookings = display_clients_bookings(client_id)
            if not bookings:
                messagebox.showinfo(
                    "Résultat", "Aucune réservation trouvée pour ce client."
                )
                return

            texte = "\n".join(
                [
                    f"Date: {res['date']}, Heure: {res['start_hour']} - {res['end_hour']}, room: {res['room_id']}"
                    for res in bookings
                ]
            )
            messagebox.showinfo("Réservations", texte)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    ttk.Button(top, text="Rechercher", command=rechercher_bookings).pack(pady=10)


def recreate_and_display_booking_section() -> None:
    """Recreate and display the reservation section."""
    global section_reserver
    section_reserver = create_booking_section()
    display_section(section_reserver)


def menu_principal() -> None:
    """Initialize the main menu and sections of the application."""
    global root
    global add_section, display_section, home_section, display_section_frame

    root = tk.Tk()
    root.title("MeetingPro - Accueil")
    root.geometry("800x700")
    root.resizable(False, False)
    root.configure(bg="#f0f8ff")

    """Style configuration."""
    menu_bar = tk.Menu(root)
    menu_bar.add_command(label="Accueil", command=lambda: display_section(home_section))
    menu_bar.add_command(label="Ajouter", command=lambda: display_section(add_section))
    menu_bar.add_command(label="Réserver", command=recreate_and_display_booking_section)
    menu_bar.add_command(
        label="Afficher", command=lambda: display_section(display_section_frame)
    )
    root.config(menu=menu_bar)

    """Style configuration for ttk."""
    home_section = ttk.Frame(root, style="TFrame")
    ttk.Label(
        home_section,
        text="Bienvenue sur MeetingPro",
        font=("Helvetica", 20, "bold"),
        background="#f0f8ff",
    ).pack(pady=20)

    """Button frame for the main menu."""
    button_frame = ttk.Frame(home_section, style="TFrame")
    button_frame.pack(pady=50)
    ttk.Button(
        button_frame,
        text="Ajouter",
        command=lambda: display_section(add_section),
        width=20,
        style="Accent.TButton",
    ).pack(pady=10)
    ttk.Button(
        button_frame,
        text="Réserver",
        command=recreate_and_display_booking_section,
        width=20,
        style="Accent.TButton",
    ).pack(pady=10)
    ttk.Button(
        button_frame,
        text="Afficher",
        command=lambda: display_section(display_section_frame),
        width=20,
        style="Accent.TButton",
    ).pack(pady=10)

    """Create sections."""
    add_section = create_add_section()
    display_section_frame = create_display_section()  # Renommé pour éviter le conflit

    """Display the home section by default."""
    display_section(home_section)

    root.mainloop()


if __name__ == "__main__":
    menu_principal()
