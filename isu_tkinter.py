import sqlite3
from hashlib import sha256
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import ttk
# NOTE: to install PIL you need to install pillow instead of PIL
# how to install PIL from terminal run: pip install pillow
# WARNING: passwords have one pattern: id + first two letters from full_name

# Path to the database
db_file_path = 'isu_database.sqlite3'

# Colors for the dark theme
BG_COLOR = "#2E2E2E"
HEADER_COLOR = "#1E1E1E"
FG_COLOR = "#FFFFFF"
ENTRY_BG = "#3E3E3E"
ENTRY_FG = "#FFFFFF"
BUTTON_BG = "#5E5E5E"
BUTTON_FG = "#FFFFFF"
HIGHLIGHT_BG = "#00A2E8"
HEADER_HOVER_BG = "#606060"
TABLE_HEADER_BG = "#444444"
TABLE_HEADER_FG = "#FFFFFF"
TABLE_ROW_BG = "#3E3E3E"
TABLE_ROW_FG = "#FFFFFF"
TABLE_SELECTED_BG = "#505050"  # Background color for selected rows
TABLE_SELECTED_FG = "#FFFFFF"  # Text color for selected rows

# Font settings
FONT_REGULAR = ("Arial", 11)
FONT_BOLD = ("Arial", 11, "bold")


# Hashing the password
def hash_password(password):
    return sha256(password.encode()).hexdigest()


# Authentication function
def authenticate(user_id, password):
    try:
        with sqlite3.connect(db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, password FROM isu_list WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if not result:
                return False, "ID not found"

            full_name, stored_password = result
            expected_password = f"{user_id}{full_name[:2]}"
            hashed_password = hash_password(expected_password)

            if hashed_password != password:
                return False, "Incorrect password"

            return True, full_name
    except Exception as e:
        return False, str(e)


# Login window
def login_window():
    def handle_login(event=None):
        user_id = entry_id.get()
        password = entry_password.get()

        if not user_id.isdigit():
            label_hint.config(text="ID must be a number", fg="red")
            return

        hashed_input_password = hash_password(password)
        is_authenticated, message = authenticate(int(user_id), hashed_input_password)

        if is_authenticated:
            auth_root.destroy()
            main_window(int(user_id))
        else:
            label_hint.config(text=message, fg="red")

    # Universal copy, cut, paste, and select-all handling
    def universal_bindings(entry):
        def handle_shortcut(event):
            # Keycodes for 'C', 'X', 'V', and 'A' on any layout
            if event.state & 0x4:  # Check if Control key is pressed
                if event.keycode == 86:  # 'V'
                    entry.event_generate("<<Paste>>")
                    return "break"
                elif event.keycode == 88:  # 'X'
                    entry.event_generate("<<Cut>>")
                    return "break"
                elif event.keycode == 67:  # 'C'
                    entry.event_generate("<<Copy>>")
                    return "break"
                elif event.keycode == 65:  # 'A'
                    entry.select_range(0, tk.END)
                    entry.icursor(tk.END)
                    return "break"
            # Let other keys function normally
            return None

        # Bind key press events
        entry.bind("<KeyPress>", handle_shortcut)

    # Login window UI
    auth_root = tk.Tk()
    auth_root.title("Login")
    auth_root.geometry("300x250")
    auth_root.resizable(False, False)
    auth_root.configure(bg=BG_COLOR)

    tk.Label(auth_root, text="Enter ID:", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    entry_id = tk.Entry(auth_root, font=FONT_REGULAR, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
    entry_id.pack(pady=5)
    universal_bindings(entry_id)

    tk.Label(auth_root, text="Enter password:", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    entry_password = tk.Entry(auth_root, show="*", font=FONT_REGULAR, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
    entry_password.pack(pady=5)
    universal_bindings(entry_password)

    label_hint = tk.Label(auth_root, text="Enter your credentials", font=FONT_REGULAR, bg=BG_COLOR, fg=FG_COLOR)
    label_hint.pack(pady=5)

    login_button = tk.Button(auth_root, text="Login", command=handle_login, font=FONT_BOLD, bg=BUTTON_BG, fg=BUTTON_FG)
    login_button.pack(pady=10)

    # Add custom header decoration
    tk.Frame(auth_root, height=3, bg=HEADER_COLOR).pack(fill=tk.X)

    auth_root.bind('<Return>', handle_login)
    auth_root.mainloop()


def main_window(user_id):
    def create_window():
        root = tk.Tk()
        root.title("Database Viewer")
        root.geometry("800x700")
        root.resizable(False, False)

        # Create style for the table
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=TABLE_ROW_BG,
                        foreground=TABLE_ROW_FG,
                        rowheight=23,
                        fieldbackground=TABLE_ROW_BG)
        style.map("Treeview",
                  background=[('selected', TABLE_SELECTED_BG)],
                  foreground=[('selected', TABLE_SELECTED_FG)])

        style.configure("Treeview.Heading",
                        background=TABLE_HEADER_BG,
                        foreground=TABLE_HEADER_FG,
                        font=FONT_BOLD)
        style.map("Treeview.Heading",
                  background=[("active", HEADER_HOVER_BG)],
                  foreground=[("active", FG_COLOR)])

        # Frames for table and photo
        frame_table = tk.Frame(root)
        frame_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def handle_shortcut(event):
            # Keycodes for 'C', 'X', 'V', and 'A' on any layout
            if event.state & 0x4:  # Check if Control key is pressed
                if event.keycode == 87:  # 'W'
                    root.mainloop()
                    return 'break'
            # Let other keys function normally
            return None

        root.bind("<KeyPress>", handle_shortcut)

        # Get number of rows in the database
        def get_row_count():
            with sqlite3.connect(db_file_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM isu_list")
                return cursor.fetchone()[0]

        row_count = get_row_count()

        # Create the table
        tree = ttk.Treeview(
            frame_table,
            columns=("Row", "ID", "Passbook Number", "Full Name"),
            show="headings",
            height=row_count + 1  # Number of rows in DB + 1 for header
        )

        # Set fixed width for the photo frame
        frame_photo = tk.Frame(root, bg=HEADER_COLOR, width=200, height=600)  # Fixed width and height
        frame_photo.pack(side=tk.RIGHT, fill=tk.Y)  # Fill vertically only
        frame_photo.pack_propagate(False)  # Prevent resizing of frame based on content

        # Photo label
        photo_label = tk.Label(frame_photo, text="Photo", bg=HEADER_COLOR, font=("Arial", 14), fg=FG_COLOR)
        photo_label.pack(pady=10)

        # Widget to display photo
        image_label = tk.Label(frame_photo, bg=HEADER_COLOR, width=250, height=300, anchor="center")  # Fixed size
        image_label.pack(padx=10, pady=10)

        # Create the table
        tree = ttk.Treeview(frame_table, columns=("Row", "ID", "Passbook Number", "Full Name"), show="headings", height=23)

        # Sorting states
        sort_states = {"ID": "asc", "Passbook Number": "asc", "Full Name": "asc"}

        # Fetch data with sorting
        def fetch_data(order_by="full_name", ascending=True):
            with sqlite3.connect(db_file_path) as conn:
                cursor = conn.cursor()
                order = "ASC" if ascending else "DESC"
                cursor.execute(f"SELECT id, passbook_number, full_name FROM isu_list ORDER BY {order_by} {order}")
                return cursor.fetchall()

        # Populate table
        def populate_table(data):
            for row in tree.get_children():
                tree.delete(row)
            for index, row in enumerate(data, start=1):
                tree.insert("", "end", values=(index, row[0], row[1], row[2]))

        # Sorting logic
        def sort_by(column):
            ascending = sort_states[column] == "desc"
            sort_states[column] = "asc" if ascending else "desc"

            # Remove indicators from all headers
            for col in ("ID", "Passbook Number", "Full Name"):
                tree.heading(col, text=col)

            # Update header text with sorting indicator only for the active column
            indicator = " ▲" if ascending else " ▼"
            tree.heading(column, text=f"{column}{indicator}")

            # Fetch and populate sorted data
            data = fetch_data(order_by=column.lower().replace(" ", "_"), ascending=ascending)
            populate_table(data)

        # Create header buttons for sorting
        tree.heading("Row", text="Row", anchor="center")  # No sorting for the Row column
        tree.column("Row", width=45, anchor="center")

        for col in ("ID", "Passbook Number", "Full Name"):
            tree.heading(col, text=col, anchor="center", command=lambda col=col: sort_by(col))
            tree.column(col, anchor="center")

        # Populate table initially with default sorting (by "Full Name")
        data = fetch_data(order_by="full_name", ascending=True)
        populate_table(data)
        # Set default sort indicator
        tree.heading("Full Name", text="Full Name ▲")

        tree.pack(fill=tk.BOTH, expand=True)

        # Handle row selection
        def on_select(event):
            selected_item = tree.selection()
            if selected_item:
                item_data = tree.item(selected_item[0])["values"]
                photo_id = item_data[1]
                display_photo(photo_id)

        # Function to display photo
        def display_photo(photo_id):
            with sqlite3.connect(db_file_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT photo FROM isu_list WHERE id = ?", (photo_id,))
                photo = cursor.fetchone()
                if photo and photo[0]:
                    image_data = io.BytesIO(photo[0])
                    pil_image = Image.open(image_data)

                    # Resize the image to fit the label's dimensions
                    pil_image.thumbnail((250, 300))  # Resize while maintaining aspect ratio

                    # Convert image to Tkinter format
                    tk_image = ImageTk.PhotoImage(pil_image)

                    # Update photo label
                    image_label.config(image=tk_image, text="")
                    image_label.image = tk_image  # Keep a reference to avoid garbage collection
                else:
                    # If no photo is available, show a placeholder or reset the image
                    image_label.config(image="", text="No Image Available", fg=FG_COLOR, font=FONT_REGULAR)

        # Select the user row in the table and load their photo
        def select_user_row(user_id):
            for row_id in tree.get_children():
                row_data = tree.item(row_id)["values"]
                if row_data[1] == user_id:
                    tree.selection_set(row_id)
                    tree.see(row_id)
                    tree.focus(row_id)
                    display_photo(user_id)
                    break

        select_user_row(user_id)

        tree.bind("<<TreeviewSelect>>", on_select)

        root.mainloop()

    create_window()


# Entry point
if __name__ == "__main__":
    login_window()
