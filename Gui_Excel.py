import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class ExcelPage(tk.Frame):
    def __init__(self, master, show_entry_page):
        print("Excel page activated")

        super().__init__(master)

        # Sayfa başlığı
        tk.Label(self, text="Excel Birleştirme", font=("Arial", 18, "bold")).pack(pady=20)

        # Bilgi etiketi
        tk.Label(self, text="Burada Excel birleştirme işlemleri yapılabilir.", font=("Arial", 12)).pack(pady=10)

        # Dosya seçme düğmesi
        tk.Button(
            self,
            text="Dosyaları Seç ve Birleştir",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.birlestir
        ).pack(pady=10)

        # Geri düğmesi
        tk.Button(
            self,
            text="Geri",
            font=("Arial", 14),
            bg="gray",
            fg="white",
            command=show_entry_page  # Ana sayfaya dönüş fonksiyonu
        ).pack(pady=20)

    def birlestir(self):
        # Excel dosyalarını seç
        file_paths = filedialog.askopenfilenames(
            title="Excel Dosyalarını Seç",
            filetypes=(
                ("Excel ve CSV Dosyaları", "*.xlsx;*.csv"),  # Hem .xlsx hem de .csv gösterir
                ("Excel Dosyaları", "*.xlsx"),
                ("CSV Dosyaları", "*.csv"),
                ("Tüm Dosyalar", "*.*")
            )
        )

        if not file_paths:
            messagebox.showwarning("Uyarı", "Herhangi bir dosya seçilmedi.")
            return

        try:
            # Tüm dosyaları oku ve birleştir
            dataframes = []
            # DESTINATION_FOLDER = os.path.dirname(file_paths[1])  # Excel dosyasının bulunduğu klasör
            # print(DESTINATION_FOLDER)
            for file in file_paths:
                if file.endswith('.xlsx'):
                    df = pd.read_excel(file)  # Excel dosyasını oku
                elif file.endswith('.csv'):
                    df = pd.read_csv(file)  # CSV dosyasını oku
                else:
                    messagebox.showwarning("Uyarı", f"Desteklenmeyen dosya formatı: {file}")
                    continue

                dataframes.append(df)

            if not dataframes:
                messagebox.showerror("Hata", "Hiçbir dosya işlenemedi!")
                return

            combined_df = pd.concat(dataframes, ignore_index=True)
            save_path_name = f"Birlesik_{len(file_paths)}_dosya.xlsx"

            # Birleştirilen dosyayı kaydet
            save_path = filedialog.asksaveasfilename(
                title="Birleştirilmiş Dosyayı Kaydet",
                defaultextension=".xlsx",
                filetypes=(("Excel Dosyaları", "*.xlsx"),)
            )

            if save_path:
                combined_df.to_excel(save_path, index=False)
                messagebox.showinfo("Başarılı", "Dosyalar başarıyla birleştirildi ve kaydedildi!")
            else:
                messagebox.showinfo("İptal", "Dosya kaydedilmedi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")