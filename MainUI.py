import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox, ttk

class MainUI:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Reservasi"]
        ctk.set_appearance_mode("Light")
        self.app = ctk.CTk()
        self.app.geometry("1200x700")
        self.app.title("Manajemen Reservasi Restoran")

        self.root_frame = ctk.CTkFrame(self.app, fg_color=("#FF6969"))
        self.root_frame.pack(fill="both", expand=True)

        self.main_frame = ctk.CTkFrame(
            self.root_frame,
            fg_color="#FFF5E0",
            bg_color="#FF6969",
            border_width=5,
            border_color="#C80036",
            corner_radius=15,
        )
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        self.side_frame = ctk.CTkFrame(
            self.main_frame,
            width=250,
            height=400,
            border_width=5,
            border_color="#C80036",
            fg_color="#FF6969",
        )
        self.side_frame.pack(side="left", fill="y", padx=25, pady=25)

        self.collections_label = ctk.CTkLabel(
            self.side_frame,
            text="Pilih Koleksi",
            font=ctk.CTkFont(size=15, weight="bold", family="JetBrains Mono"),
            text_color="#FFF5E0",
        )
        self.collections_label.pack(pady=(10, 5))

        # Ambil List Koleksi
        collections = list(self.db.list_collection_names())

        # Pemilihan Koleksi dengan Dropdown
        self.selected_collection = ctk.StringVar(value=collections[0])
        self.collections_dropdown = ctk.CTkOptionMenu(
            self.side_frame,
            fg_color="#FFF5E0",
            text_color="#FF6969",
            button_color="#C80036",
            button_hover_color="#0C1844",
            dropdown_fg_color="#FFF5E0",
            dropdown_text_color="#0C1844",
            dropdown_hover_color="#FF6969",
            dropdown_font=ctk.CTkFont(
                size=13, weight="normal", family="JetBrains Mono"
            ),
            font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
            values=collections,
            variable=self.selected_collection,
            # command = Isi fungsi menampilkan data
        )
        self.collections_dropdown.pack(pady=10, padx=20)

        self.crud_frame = ctk.CTkFrame(
            self.side_frame, fg_color="transparent", width=169
        )
        self.crud_frame.pack(pady=10)

        self.insert_bt = ctk.CTkButton(
            self.crud_frame,
            text="INSERT",
            fg_color="#FFF5E1",
            bg_color="#FF6969",
            text_color="#FF6969",
            border_color="#C80036",
            border_width=3,
            hover=True,
            hover_color="#0C1844",
            width=70,
            font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
        )
        self.insert_bt.grid(row=0, column=0, padx=5, pady=5)
        
        self.delete_bt = ctk.CTkButton(
            self.crud_frame,
            text="DELETE",
            fg_color="#FFF5E1",
            bg_color="#FF6969",
            text_color="#FF6969",
            border_color="#C80036",
            border_width=3,
            hover=True,
            hover_color="#0C1844",
            width=70,
            font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
        )
        self.delete_bt.grid(row=0, column=1, padx=5, pady=5)
        
        self.update_bt = ctk.CTkButton(
            self.crud_frame,
            text="UPDATE",
            fg_color="#FFF5E1",
            bg_color="#FF6969",
            text_color="#FF6969",
            border_color="#C80036",
            border_width=3,
            hover=True,
            hover_color="#0C1844",
            width=70,
            font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
        )
        self.update_bt.grid(row=1, column=0, columnspan=2, pady=5)

    def run(self):
        self.app.mainloop()


def main_ui():
    app = MainUI()
    app.run()

main_ui()
