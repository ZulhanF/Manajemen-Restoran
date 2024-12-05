import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox


MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Restoran"
COLLECTION_NAME = "Admin"


def verify_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
        return

    # Koneksi ke MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Pencarian username dan password
    user = collection.find_one({"username": username, "password": password})

    if user:
        messagebox.showinfo("Success", "Login berhasil!")
    else:
        messagebox.showerror("Error", "Username atau password salah!")

    # Tutup koneksi
    client.close()


# Konfigurasi tampilan CustomTkinter
ctk.set_appearance_mode("Light")
app = ctk.CTk()
app.geometry("430x370")
app.title("Login Page")

root_frame = ctk.CTkFrame(
    app, fg_color=("#FF6969")
)
root_frame.pack(fill="both", expand=True)


main_frame = ctk.CTkFrame(
    root_frame,
    fg_color="#FFF5E0",
    bg_color="#FF6969",
    border_width=5,
    border_color="#C80036",
    corner_radius=15,
)
main_frame.pack(fill="both", expand=True, padx=25, pady=25)

# Label judul di atas
title_label = ctk.CTkLabel(
    main_frame,
    text="Selamat Datang!",
    font=ctk.CTkFont(size=24, family="JetBrains Mono"),
)
title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

# Label dan input username
username_label = ctk.CTkLabel(
    main_frame, text="Username:", font=ctk.CTkFont(size=14, family="JetBrains Mono")
)
username_label.grid(row=1, column=0, padx=30, pady=5, sticky="w")
username_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Masukkan username",
    width=300,
    border_width=2,
    border_color="#C80036",
    fg_color="#FFFFFF",
    font=ctk.CTkFont(size=13,family="Cascadia Mono")
)
username_entry.grid(row=2, column=0, padx=30, pady=0, sticky="ew")

# Label dan input password
password_label = ctk.CTkLabel(
    main_frame, text="Password:", font=ctk.CTkFont(size=14, family="JetBrains Mono")
)
password_label.grid(row=3, column=0, padx=30, pady=5, sticky="w")
password_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Masukkan password",
    show="*",
    width=300,
    border_width=2,
    border_color="#C80036",
    fg_color="#FFFFFF",
    font=ctk.CTkFont(size=13,family="Cascadia Mono")
)
password_entry.grid(row=4, column=0, padx=30, pady=0, sticky="w")

# Tombol login
login_button = ctk.CTkButton(
    main_frame,
    text="Login",
    command=verify_login,
    font=ctk.CTkFont(size=14, weight="bold", family="Poppins", underline="true" ),
    text_color="#FFF5E0",
    hover=True,
    hover_color="#d94e4e",
    height=40,
    width=100,
    border_width=3,
    corner_radius=10,
    border_color="#C80036",
    bg_color="transparent",
    fg_color="#FF6969",
)
login_button.grid(row=5, column=0, padx=30, pady=20, sticky="w")

# Menjalankan aplikasi
app.mainloop()
