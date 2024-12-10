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
            text="Pilih Koleksi:",
            font=ctk.CTkFont(size=15, weight="bold", family="JetBrains Mono"),
            text_color="#FFF5E0",
        )
        self.collections_label.pack(pady=(10, 5))

        collections = list(self.db.list_collection_names())

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
            command=self.load_collection_data,
        )
        self.collections_dropdown.pack(pady=10, padx=20)

        self.crud_frame = ctk.CTkFrame(
            self.side_frame, fg_color="transparent", width=169
        )
        self.crud_frame.pack(pady=10)

        # Tombol insert
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
            command=self.insert_data,
        )
        self.insert_bt.grid(row=0, column=0, padx=5, pady=5)

        # Tombol delete
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
            command=self.delete_data,
        )
        self.delete_bt.grid(row=0, column=1, padx=5, pady=5)

        # Tombol update
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
            command=self.update_data,
        )
        self.update_bt.grid(row=1, column=0, padx=5, pady=5)
        
        # Tombol find
        self.find_bt = ctk.CTkButton(
            self.crud_frame,
            text="FIND",
            fg_color="#FFF5E1",
            bg_color="#FF6969",
            text_color="#FF6969",
            border_color="#C80036",
            border_width=3,
            hover=True,
            hover_color="#0C1844",
            width=70,
            font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
            command=self.find_data,
        )
        self.find_bt.grid(row=1, column=1, padx=5, pady=5)

        self.sort_field_label = ctk.CTkLabel(
            self.side_frame,
            text="Urutkan Field:",
            font=ctk.CTkFont(size=15, weight="bold", family="JetBrains Mono"),
            text_color="#FFF5E0",
        )
        self.sort_field_label.pack(pady=(10, 5))

        self.sort_field_var = ctk.StringVar(value="")
        self.sort_field_dropdown = ctk.CTkOptionMenu(
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
            values=[],
            variable=self.sort_field_var,
        )
        self.sort_field_dropdown.pack(pady=10, padx=20)

        self.sort_option = ["Ascending", "Descending"]
        self.sort_var = ctk.StringVar(value=self.sort_option[0])

        self.sort_dropdown = ctk.CTkOptionMenu(
            self.side_frame,
            values=self.sort_option,
            variable=self.sort_var,
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
            command=self.sort_treeview,
        )
        self.sort_dropdown.pack(pady=10)

        self.sort_button = ctk.CTkButton(
            self.side_frame,
            text="Sorting",
            fg_color="#FFF5E1",
            bg_color="#FF6969",
            text_color="#FF6969",
            border_color="#C80036",
            border_width=3,
            hover=True,
            hover_color="#0C1844",
            width=70,
            font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
            command=self.sort_treeview,
        )
        self.sort_button.pack(pady=10)
        
        self.agregasi_label = ctk.CTkLabel(
            self.side_frame,
            text="Advanced View:",
            font=ctk.CTkFont(size=15, weight="bold", family="JetBrains Mono"),
            text_color="#FFF5E0",
        )
        self.agregasi_label.pack(pady=(10, 5))

        self.agregasi_options = [
            "Pelanggan Teratas", 
            "Waktu Reservasi Terpopuler", 
            "Menu Terlaris"
        ]
        self.agregasi_var = ctk.StringVar(value="Pilih Agregasi")

        self.agregasi_dropdown = ctk.CTkOptionMenu(
            self.side_frame,
            values=self.agregasi_options,
            variable=self.agregasi_var,
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
            command=self.run_agregation,
        )
        self.agregasi_dropdown.pack(pady=10, padx=20)

        # Tombol untuk menjalankan agregasi, sementara dihilangkan.
        # self.agregasi_button = ctk.CTkButton(
        #     self.side_frame,
        #     text="Jalankan Agregasi",
        #     fg_color="#FFF5E1",
        #     bg_color="#FF6969",
        #     text_color="#FF6969",
        #     border_color="#C80036",
        #     border_width=3,
        #     hover=True,
        #     hover_color="#0C1844",
        #     width=70,
        #     font=ctk.CTkFont(size=13, weight="bold", family="JetBrains Mono"),
        #     command=self.run_agregation,
        # )
        # self.agregasi_button.pack(pady=10)

            # Main Frame kanan untuk menampilkan data dari koleksi yang dipilih
        self.data_frame = ctk.CTkFrame(
                self.main_frame,
                fg_color="#FF6969",
                corner_radius=15,
                border_width=5,
                border_color="#C80036",
            )
        self.data_frame.pack(side="right", fill="both", expand=True, padx=25, pady=25)

            # Inisialisasi tabel treeview ke mainframe kanan
        self.tree_scroll = ctk.CTkFrame(self.data_frame, fg_color="transparent")
        self.tree_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.tree_scroll)
        self.tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#FFF5E0",
            foreground="#0C1844",
            rowheight=45,
            fieldbackground="#FFF5E0",
            font=("JetBrains Mono", 17),
        )

        style.configure(
            "Treeview.Heading",
            foreground="#FF6969",
            font=("JetBrains Mono", 19, "bold"),
            rowheight=47,
        )
        style.map(
            "Treeview",
            background=[("selected", "#C80036")],
        )

        if collections and collections[0] != "Tidak ada koleksi":
            self.load_collection_data(collections[0])

    def load_collection_data(self, collection_name=None, sort_order="Ascending"):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if collection_name is None:
            collection_name = self.selected_collection.get()
        collection = self.db[collection_name]
        try:
            documents = list(collection.find())
            if documents:
                columns = list(documents[0].keys())
                columns = [col for col in columns if col != "_id"]

                self.sort_field_dropdown.configure(values=columns)
                if not self.sort_field_var.get():
                    self.sort_field_var.set(columns[0])  # Set default field

                self.tree["columns"] = columns
                self.tree["show"] = "headings"
                for col in columns:
                    self.tree.heading(col, text=col.title(), anchor="center")
                    self.tree.column(col, anchor="center", width=150)

            sort_field = self.sort_field_var.get()
            sort_order = self.sort_var.get()

            if sort_field:
                try:
                    documents.sort(
                        key=lambda x: x.get(sort_field, ""),
                        reverse=(sort_order == "Descending"),
                    )
                except TypeError:
                    documents.sort(
                        key=lambda x: str(x.get(sort_field, "")),
                        reverse=(sort_order == "Descending"),
                    )

            for doc in documents:
                row_data = [str(doc.get(col, "")) for col in columns]
                self.tree.insert("", "end", values=row_data)

            if not documents:
                messagebox.showinfo(
                    "Info", f"Tidak ada data dalam koleksi {collection_name}"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")

    def sort_treeview(self):
        collection_name = self.selected_collection.get()
        self.load_collection_data(collection_name)
        
    def find_data(self):
        collection_name = self.selected_collection.get()
        collection = self.db[collection_name]
        
        search_term = ctk.CTkInputDialog(
            title="Cari Data",
            text="Masukkan nilai yang ingin dicari(Akan dicari di semua field koleksi ini😋) :",
            font=ctk.CTkFont(size=14, family="JetBrains Mono"),
            button_fg_color="#FF6969",
            button_hover_color="#C80036",
            fg_color="#FFF5E0",
            entry_border_color="#C80036",
            button_text_color="#0C1844",
        ).get_input()
        
        if search_term is None or search_term.strip() == "":
            return

        try:
            for i in self.tree.get_children():
                self.tree.delete(i)

            sample_doc = collection.find_one()
            if not sample_doc:
                messagebox.showinfo("Info", "Koleksi Kosong")
                return

            columns = list(sample_doc.keys())
            columns = [col for col in columns if col != "_id"]
            
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            for col in columns:
                self.tree.heading(col, text=col.title(), anchor="center")
                self.tree.column(col, anchor="center", width=150)

            query = {
                "$or": [
                    {col: {"$regex": search_term, "$options": "i"}} 
                    for col in columns
                ]
            }

            matching_docs = list(collection.find(query))

            if matching_docs:
                for doc in matching_docs:
                    row_data = [str(doc.get(col, "")) for col in columns]
                    self.tree.insert("", "end", values=row_data)
                
                messagebox.showinfo("Hasil Pencarian", f"Menemukan {len(matching_docs)} data yang sesuai")
            else:
                messagebox.showinfo("Hasil Pencarian", "Tidak ada data yang sesuai")

        except Exception as e:
            messagebox.showerror("Error", f"Find Gagal: {str(e)}")

    def insert_data(self):
        collection = self.db[self.selected_collection.get()]
        new_data = {}
        for key in list(collection.find_one()):
            value = ctk.CTkInputDialog(
                title="Masukkan Data",
                text=f"Masukkan Nilai '{key}':",
                font=ctk.CTkFont(size=14, family="JetBrains Mono"),
                button_fg_color="#FF6969",
                button_hover_color="#C80036",
                fg_color="#FFF5E0",
                entry_border_color="#C80036",
                button_text_color="#0C1844",
            ).get_input()
            if value is None:
                return
            new_data[key] = value
        inserted_id = collection.insert_one(new_data).inserted_id
        print(f"Data baru masuk dengan id: {inserted_id}")
        messagebox.showinfo("Succes!",f"Data berhasil ditambahkan")
        self.load_collection_data(None)

    def delete_data(self):
        collection = self.db[self.selected_collection.get()]
        doc_id = ctk.CTkInputDialog(
            title="Hapus Data",
            text="Masukkan ID Data yang ingin dihapus: 🗑️",
            font=ctk.CTkFont(size=14, family="JetBrains Mono"),
            button_fg_color="#FF6969",
            button_hover_color="#C80036",
            fg_color="#FFF5E0",
            entry_border_color="#C80036",
            button_text_color="#0C1844",
        ).get_input()
        if doc_id is None:
            return

        collection.delete_one({"_id": doc_id})
        messagebox.showinfo("Succes!",f"Data dengan ID {doc_id} berhasil dihapus")
        self.load_collection_data(None)

    def update_data(self):
        collection = self.db[self.selected_collection.get()]
        doc_id = ctk.CTkInputDialog(
            title="Perbarui Data",
            text="Masukkan ID Data yng ingin diperbarui: ⬆",
            font=ctk.CTkFont(size=14, family="JetBrains Mono"),
            button_fg_color="#FF6969",
            button_hover_color="#C80036",
            fg_color="#FFF5E0",
            entry_border_color="#C80036",
            button_text_color="#0C1844",
        ).get_input()
        if doc_id is None:
            return

        existing_doc = collection.find_one({"_id": doc_id})
        if not existing_doc:
            messagebox.showerror("Error", f"Data dengan ID '{doc_id}' tidak ditemukan.")
            return

        new_data = {}
        for key, value in existing_doc.items():
            new_value = ctk.CTkInputDialog(
                title="Update Data",
                text=f"Enter new value for '{key}' (current value: {value}):",
                font=ctk.CTkFont(size=14, family="JetBrains Mono"),
                button_fg_color="#FF6969",
                button_hover_color="#C80036",
                fg_color="#FFF5E0",
                entry_border_color="#C80036",
                button_text_color="#0C1844",
            ).get_input()
            if new_value is None:
                return
            new_data[key] = new_value if new_value else value

        collection.update_one({"_id": doc_id}, {"$set": new_data})
        messagebox.showinfo("Succes!",f"Data dengan ID {doc_id} berhasil diperbarui")
        self.load_collection_data(None)
    
    def run_agregation(self, agregasi_pilihan=None):
        agregasi_pilihan = self.agregasi_var.get()
        
        try:

            for i in self.tree.get_children():
                self.tree.delete(i)

            if agregasi_pilihan == "Pelanggan Teratas":
                result = list(self.db.Transaksi.aggregate([
                    {
                        '$lookup': {
                            'from': "Reservasi",
                            'localField': "ID_RESERVASI",
                            'foreignField': "_id",
                            'as': "reservasiInfo"
                        }
                    },
                    {
                        '$unwind': "$reservasiInfo"
                    },
                    {
                        '$lookup': {
                            'from': "Pelanggan",
                            'localField': "reservasiInfo.ID_PELANGGAN",
                            'foreignField': "ID_PELANGGAN",
                            'as': "pelangganInfo"
                        }
                    },
                    {
                        '$unwind': "$pelangganInfo"
                    },
                    {
                        '$group': {
                            '_id': "$pelangganInfo.ID_PELANGGAN",
                            'namaPelanggan': { '$first': "$pelangganInfo.NAMA" },
                            'totalPengeluaran': { '$sum': "$TOTAL_HARGA" },
                            'totalReservasi': { '$sum': 1 }
                        }
                    },
                    {
                        '$project': {
                            '_id': 0,
                            'Nama Pelanggan': "$namaPelanggan",
                            'Total Pengeluaran': "$totalPengeluaran",
                            'Total Reservasi': "$totalReservasi"
                        }
                    },
                    { '$sort': { 'Total Reservasi': -1, 'Total Pengeluaran':-1 } }
                ]))

                
            elif agregasi_pilihan == "Waktu Reservasi Terpopuler":
                result = list(self.db.Reservasi.aggregate([
                    {
                        '$group': {
                            '_id': "$WAKTU", 
                            'totalReservasi': { '$sum': 1 }
                        }
                    },
                    {
                        '$project': {
                            '_id': 0,
                            'Waktu': "$_id",
                            'Total Reservasi': "$totalReservasi"
                        }
                    },
                    { '$sort': { 'Total Reservasi': -1 } }
                ]))
                
            elif agregasi_pilihan == "Menu Terlaris":
                result = list(self.db.DetailPesanan.aggregate([
                    {
                        '$group': {
                        '_id': { 'ID_MENU': "$ID_MENU", 'Nama_Menu': "$NAMA_MENU", 'Kategori': "$KATEGORI_MENU" },
                        'TotalPesanan': { '$sum': "$JUMLAH" }
                        }
                    },
                    {
                        '$project': {
                        '_id': 0,
                        "ID Menu": "$_id.ID_MENU",
                        "Nama Menu": "$_id.Nama_Menu",
                        "Kategori": "$_id.Kategori",
                        "Total Pesanan": "$TotalPesanan"
                        }
                    },
                    { '$sort': { "Total Pesanan": -1 } }
                    ]))
            
            if not result:
                messagebox.showinfo("Informasi", "Tidak ada data yang ditemukan")
                return

            columns = list(result[0].keys())
            
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            for col in columns:
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, anchor="center", width=200)

            for doc in result:
                row_data = [str(doc.get(col, "")) for col in columns]
                self.tree.insert("", "end", values=row_data)

            messagebox.showinfo("Sukses", f"Agregasi {agregasi_pilihan} berhasil dijalankan")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal menjalankan agregasi: {str(e)}")

    def run(self):
        self.app.mainloop()

def main_ui():
    app = MainUI()
    app.run()

#main_ui()
