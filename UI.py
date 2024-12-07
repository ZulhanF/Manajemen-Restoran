import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox, ttk
import tkinter as tk

class MainUI:
    def __init__(self):
        # Ensure CustomTkinter appearance mode
        ctk.set_appearance_mode("Light")
        
        # MongoDB Connection
        self.MONGO_URI = "mongodb://localhost:27017/"
        self.DB_NAME = "Reservasi"
        self.client = MongoClient(self.MONGO_URI)
        self.db = self.client[self.DB_NAME]

        # Main Application Window
        self.app = ctk.CTk()
        self.app.geometry("1200x700")
        self.app.title("Manajemen Reservasi")

        # Prevent multiple instances
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Sidebar
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=250, fg_color="#FF6969")
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)

        # Collections Listbox
        self.collections_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Pilih Koleksi", 
            font=ctk.CTkFont(size=18, weight="bold", family="JetBrains Mono")
        )
        self.collections_label.pack(pady=(10, 5))

        # Get collections
        collections = self.get_collections()
        
        # Ensure we have at least one collection
        if not collections:
            collections = ["Tidak ada koleksi"]

        # Collections Dropdown
        self.selected_collection = ctk.StringVar(value=collections[0])
        self.collections_dropdown = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=collections,
            variable=self.selected_collection,
            command=self.load_collection_data
        )
        self.collections_dropdown.pack(pady=10, padx=20)

        # CRUD Buttons
        self.crud_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.crud_frame.pack(pady=10)

        crud_buttons = [
            ("Tambah", self.add_record),
            ("Edit", self.edit_record),
            ("Hapus", self.delete_record)
        ]

        for text, command in crud_buttons:
            btn = ctk.CTkButton(
                self.crud_frame, 
                text=text, 
                command=command,
                font=ctk.CTkFont(size=14, family="Poppins"),
                width=150
            )
            btn.pack(pady=5)

        # Right Data Display Area
        self.data_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFF5E0")
        self.data_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for Treeview
        self.tree_frame = ctk.CTkFrame(self.data_frame)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview with Scrollbar
        self.tree_scroll = ctk.CTkScrollableFrame(self.tree_frame)
        self.tree_scroll.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_scroll)
        self.tree.pack(fill="both", expand=True)

        # Initial load of first collection
        if collections and collections[0] != "Tidak ada koleksi":
            self.load_collection_data(collections[0])

    def get_collections(self):
        # Get list of collections in the database
        try:
            return list(self.db.list_collection_names())
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mendapatkan daftar koleksi: {str(e)}")
            return []

    def load_collection_data(self, collection_name=None):
        # Clear existing data
        for i in self.tree.get_children():
            self.tree.delete(i)

        # If no collection name provided, use the selected one
        if collection_name is None:
            collection_name = self.selected_collection.get()

        # Get selected collection
        collection = self.db[collection_name]

        try:
            # Fetch data
            documents = list(collection.find())

            if documents:
                # Set columns based on first document's keys
                columns = list(documents[0].keys())
                columns = [col for col in columns if col != '_id']
                
                # Configure treeview
                self.tree['columns'] = columns
                
                # Remove old headings
                for col in self.tree['columns']:
                    self.tree.heading(col, text='')
                    self.tree.column(col, anchor='center', width=100)
                
                # Create column headings
                for col in columns:
                    self.tree.heading(col, text=col)

                # Insert data
                for doc in documents:
                    # Convert ObjectId to string for display
                    row_data = [str(doc.get(col, '')) for col in columns]
                    self.tree.insert('', 'end', values=row_data)
            else:
                messagebox.showinfo("Info", f"Tidak ada data dalam koleksi {collection_name}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")

    def add_record(self):
        # Placeholder for adding a new record
        messagebox.showinfo("Tambah Record", "Fitur tambah record akan segera hadir!")

    def edit_record(self):
        # Placeholder for editing a record
        messagebox.showinfo("Edit Record", "Fitur edit record akan segera hadir!")

    def delete_record(self):
        # Placeholder for deleting a record
        messagebox.showinfo("Hapus Record", "Fitur hapus record akan segera hadir!")

    def on_closing(self):
        # Properly close MongoDB connection
        if hasattr(self, 'client'):
            self.client.close()
        self.app.destroy()

    def run(self):
        self.app.mainloop()

def main_ui():
    app = MainUI()
    app.run()

if __name__ == "__main__":
    main_ui()