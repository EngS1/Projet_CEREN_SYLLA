import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from main import (
    add_client,
    add_room,
    get_available_rooms,
    get_clients,
    book_room,
    get_available_rooms_for_slot,
    get_client_reservations,
    load_data,
    save_data,
    validate_email,
)
import json


# Load data at startup
data_file = "data.json"
load_data(data_file)


def show_section(frame):
    """Displays a specific section and hides the others."""
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Frame):
            widget.pack_forget()
    frame.pack(fill=tk.BOTH, expand=True)


def create_add_section():
    """Creates the 'Add' section."""
    frame = ttk.Frame(root, style="TFrame")

    def show_client_form():
        """Displays the form to add a client."""
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
        entry_first_name = ttk.Entry(frame, width=40)
        entry_first_name.pack(pady=5)
        ttk.Label(frame, text="Email", background="#f0f8ff").pack(pady=5)
        entry_email = ttk.Entry(frame, width=40)
        entry_email.pack(pady=5)

        def validate_client_addition():
            """Validates the inputs and adds a client."""
            name = entry_name.get().strip()
            first_name = entry_first_name.get().strip()
            email = entry_email.get().strip()
            is_valid, _ = validate_email(email)
            if not is_valid:
                messagebox.showerror("Erreur", "Email invalide.")
                return
            if not name or not email:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return

            # Add the client
            client = add_client(name, first_name, email)
            messagebox.showinfo(
                "Succès",
                f"Client ajouté avec succès :\nID: {client['id']}\nNom: {client['name']}\nPrénom: {client['first_name']}\nEmail: {client['email']}",
            )
            save_data(data_file)

        # Buttons for Cancel and Validate
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=show_main_buttons,
            style="Secondary.TButton",
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Valider",
            command=validate_client_addition,
            style="Accent.TButton",
            width=15,
        ).pack(side=tk.RIGHT, padx=10)

    def show_room_form():
        """Displays the form to add a room."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame,
            text="Ajouter une Salle",
            font=("Helvetica", 16, "bold"),
            background="#f0f8ff",
        ).pack(pady=10)

        # Field for room name (used as ID)
        ttk.Label(frame, text="Nom de la salle (unique)", background="#f0f8ff").pack(
            pady=5
        )
        entry_room_name = ttk.Entry(frame, width=40)
        entry_room_name.pack(pady=5)
        error_room_name = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_room_name.pack()

        # Dropdown menu for room type
        ttk.Label(frame, text="Type de salle", background="#f0f8ff").pack(pady=5)
        room_type_var = tk.StringVar()
        room_type_menu = ttk.Combobox(
            frame, textvariable=room_type_var, state="readonly", width=37
        )
        room_type_menu["values"] = ["Standard", "Conférence", "Informatique"]
        room_type_menu.pack(pady=5)
        error_room_type = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_room_type.pack()

        # Field for capacity (incrementable)
        ttk.Label(frame, text="Capacité", background="#f0f8ff").pack(pady=5)
        capacity_var = tk.IntVar(value=1)  # Capacity starts at 1
        frame_capacity = ttk.Frame(frame, style="TFrame")
        frame_capacity.pack(pady=5)

        def increment_capacity():
            """Increments the capacity based on the room type."""
            room_type = room_type_var.get()
            if room_type == "Standard" or room_type == "Informatique":
                capacity_var.set(min(4, capacity_var.get() + 1))
            elif room_type == "Conférence":
                capacity_var.set(min(12, capacity_var.get() + 1))

        def decrement_capacity():
            """Decrements the capacity (minimum 1)."""
            capacity_var.set(max(1, capacity_var.get() - 1))

        ttk.Button(frame_capacity, text="-", command=decrement_capacity).pack(
            side=tk.LEFT
        )
        ttk.Label(
            frame_capacity, textvariable=capacity_var, width=5, anchor="center"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_capacity, text="+", command=increment_capacity).pack(
            side=tk.LEFT
        )

        error_capacity = ttk.Label(
            frame, text="", foreground="red", background="#f0f8ff"
        )
        error_capacity.pack()

        def validate_room():
            """Validates the inputs and adds a room."""
            room_name = entry_room_name.get().strip()  # Used as ID and name
            room_type = room_type_var.get()
            capacity = capacity_var.get()

            # Reset error messages
            error_room_name.config(text="")
            error_room_type.config(text="")
            error_capacity.config(text="")

            # Validate fields
            errors = False
            if not room_name:
                error_room_name.config(text="Veuillez entrer un nom de salle.")
                errors = True
            if not room_type:
                error_room_type.config(text="Veuillez sélectionner un type de salle.")
                errors = True
            if capacity <= 0:
                error_capacity.config(text="La capacité doit être supérieure à 0.")
                errors = True

            # Capacity limitation based on room type
            if room_type == "Standard" or room_type == "Informatique":
                if capacity > 4:
                    error_capacity.config(
                        text="La capacité maximale pour une salle Standard ou Informatique est de 4 personnes."
                    )
                    errors = True
            elif room_type == "Conférence":
                if capacity > 12:
                    error_capacity.config(
                        text="La capacité maximale pour une salle de Conférence est de 12 personnes."
                    )
                    errors = True

            if errors:
                return

            # Check for unique room name
            existing_rooms = get_available_rooms()
            if any(room["id"] == room_name for room in existing_rooms):
                error_room_name.config(
                    text=f"Le nom de la salle '{room_name}' existe déjà. Veuillez en choisir un autre."
                )
                return

            # Add the room (ID and name are identical)
            room = add_room(room_name, room_type, capacity)
            messagebox.showinfo(
                "Succès",
                f"Salle ajoutée avec succès :\nNom: {room['id']}\nType: {room['type']}\nCapacité: {room['capacity']}",
            )
            save_data(data_file)
            show_main_buttons()

        # Buttons for Cancel and Validate
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=show_main_buttons,
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

    def show_main_buttons():
        """Displays the main buttons of the 'Add' section."""
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(
            frame, text="Ajouter", font=("Helvetica", 16, "bold"), background="#f0f8ff"
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouveau client",
            command=show_client_form,
            width=35,  # Increased from 30 to 35
            style="Accent.TButton",
        ).pack(pady=10)
        ttk.Button(
            frame,
            text="Ajouter nouvelle salle",
            command=show_room_form,
            width=35,  # Increased from 30 to 35
            style="Accent.TButton",
        ).pack(pady=10)

    show_main_buttons()
    return frame


def create_main_menu():
    """Creates the main menu of the application."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Menu Principal",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)

    ttk.Button(
        frame,
        text="Ajouter",
        command=lambda: show_section(create_add_section()),
        width=30,
        style="Accent.TButton",
    ).pack(pady=10)

    ttk.Button(
        frame,
        text="Réserver une salle",
        command=lambda: show_section(create_reservation_section()),
        width=30,
        style="Accent.TButton",
    ).pack(pady=10)

    ttk.Button(
        frame,
        text="Voir les réservations",
        command=lambda: show_section(create_view_reservations_section()),
        width=30,
        style="Accent.TButton",
    ).pack(pady=10)

    return frame


def create_reservation_section():
    """Creates the 'Reservation' section."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Réserver une Salle",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)

    # Client selection
    ttk.Label(frame, text="Sélectionnez un client", background="#f0f8ff").pack(pady=5)
    client_var = tk.StringVar()
    client_menu = ttk.Combobox(
        frame, textvariable=client_var, state="readonly", width=40
    )
    client_menu["values"] = [
        f"{client['id']} - {client['name']}" for client in get_clients()
    ]
    client_menu.pack(pady=5)

    # Date and time selection
    ttk.Label(frame, text="Date de début", background="#f0f8ff").pack(pady=5)
    start_date = Calendar(frame, date_pattern="yyyy-mm-dd")
    start_date.pack(pady=5)

    ttk.Label(frame, text="Heure de début (HH:MM)", background="#f0f8ff").pack(pady=5)
    start_time = ttk.Entry(frame, width=10)
    start_time.pack(pady=5)

    ttk.Label(frame, text="Date de fin", background="#f0f8ff").pack(pady=5)
    end_date = Calendar(frame, date_pattern="yyyy-mm-dd")
    end_date.pack(pady=5)

    ttk.Label(frame, text="Heure de fin (HH:MM)", background="#f0f8ff").pack(pady=5)
    end_time = ttk.Entry(frame, width=10)
    end_time.pack(pady=5)

    def validate_reservation():
        """Validates the reservation inputs and books a room."""
        client_id = client_var.get().split(" - ")[0]
        start_datetime = f"{start_date.get_date()} {start_time.get()}"
        end_datetime = f"{end_date.get_date()} {end_time.get()}"

        try:
            start = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
            end = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date ou d'heure invalide.")
            return

        if start >= end:
            messagebox.showerror(
                "Erreur", "La date de fin doit être après la date de début."
            )
            return

        available_rooms = get_available_rooms_for_slot(start, end)
        if not available_rooms:
            messagebox.showinfo(
                "Aucune salle disponible",
                "Aucune salle n'est disponible pour ce créneau.",
            )
            return

        room = available_rooms[0]  # Automatically select the first available room
        book_room(client_id, room["id"], start, end)
        save_data(data_file)
        messagebox.showinfo("Succès", f"Salle réservée avec succès : {room['id']}")

    # Buttons for Cancel and Validate
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20)

    ttk.Button(
        button_frame,
        text="Annuler",
        command=lambda: show_section(create_main_menu()),
        style="Secondary.TButton",
        width=15,
    ).pack(side=tk.LEFT, padx=10)

    ttk.Button(
        button_frame,
        text="Valider",
        command=validate_reservation,
        style="Accent.TButton",
        width=15,
    ).pack(side=tk.RIGHT, padx=10)

    return frame


def create_view_reservations_section():
    """Creates the 'View Reservations' section."""
    frame = ttk.Frame(root, style="TFrame")

    ttk.Label(
        frame,
        text="Voir les Réservations",
        font=("Helvetica", 16, "bold"),
        background="#f0f8ff",
    ).pack(pady=10)

    reservations = get_client_reservations()
    for reservation in reservations:
        ttk.Label(
            frame,
            text=f"Client: {reservation['client_id']} | Salle: {reservation['room_id']} | Début: {reservation['start']} | Fin: {reservation['end']}",
            background="#f0f8ff",
        ).pack(pady=5)

    ttk.Button(
        frame,
        text="Retour",
        command=lambda: show_section(create_main_menu()),
        style="Secondary.TButton",
        width=15,
    ).pack(pady=20)

    return frame


# Initialize the application
root = tk.Tk()
root.title("Application de Réservation")
root.geometry("800x600")
root.configure(background="#f0f8ff")

# Show the main menu
show_section(create_main_menu())

root.mainloop()
