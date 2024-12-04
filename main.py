import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox

# Konfigurasi MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Restoran"
COLLECTION_NAME = "Admin"


# Fungsi verifikasi login
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
ctk.set_appearance_mode("Light")  # Tema: Light, Dark, System
app = ctk.CTk()
app.geometry("500x400")
app.title("Login Page")
# Tambahkan frame utama di aplikasi untuk menggantikan langsung background
root_frame = ctk.CTkFrame(
    app, fg_color=("#FF6969")
)  # Gunakan warna latar belakang yang diinginkan
root_frame.pack(fill="both", expand=True)

# Pindahkan main_frame ke dalam root_frame
main_frame = ctk.CTkFrame(root_frame, fg_color="#FFF5E0", bg_color=("#FF6969"), border_width=5, border_color="#C80036", corner_radius=15)
main_frame.pack(fill="both", expand=True, padx=25, pady=25)

# Label judul di atas
title_label = ctk.CTkLabel(
    main_frame,
    text="Login Page",
    font=ctk.CTkFont(size=24, weight="bold", family="Poppins"),
)
title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

# Label dan input username
username_label = ctk.CTkLabel(main_frame, text="Username:", font=ctk.CTkFont(size=14))
username_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
username_entry = ctk.CTkEntry(
    main_frame, placeholder_text="Masukkan username", width=300
)
username_entry.grid(row=2, column=0, padx=20, pady=5, sticky="w")

# Label dan input password
password_label = ctk.CTkLabel(main_frame, text="Password:", font=ctk.CTkFont(size=14))
password_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
password_entry = ctk.CTkEntry(
    main_frame, placeholder_text="Masukkan password", show="*", width=300
)
password_entry.grid(row=4, column=0, padx=20, pady=5, sticky="w")

# Tombol login
login_button = ctk.CTkButton(
    main_frame,
    text="Login",
    command=verify_login,
    font=ctk.CTkFont(size=12, weight="bold", family="Poppins"),
    text_color="white",
    hover=True,
    hover_color="#81b867",
    height=40,
    width=120,
    border_width=2,
    corner_radius=5,
    border_color="#608a4d",
    bg_color="#262626",
    fg_color="#79ae61",
)  # Warna kuning keemasan
login_button.grid(row=5, column=0, padx=10, pady=20, sticky="w")

# Menjalankan aplikasi
app.mainloop()
