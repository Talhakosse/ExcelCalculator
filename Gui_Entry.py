import tkinter as tk

class EntryPage(tk.Frame):
    def __init__(self, master, show_excel_page,show_email_page):
        super().__init__(master)
        print("Entry page activated")
        # Hoş geldiniz etiketi
        tk.Label(self, text="Hoş Geldiniz!", font=("Arial", 18, "bold")).pack(pady=20)

        # "Excel Birleştir" düğmesi
        tk.Button(
            self,
            text="Excel Birleştir",
            font=("Arial", 14),
            bg="blue",
            fg="white",
            command=show_excel_page  # Excel sayfasına geçiş fonksiyonunu çağırır
        ).pack(pady=10)
        # "Email_find Birleştir" düğmesi
        tk.Button(
            self,
            text="Email Tara",
            font=("Arial", 14),
            bg="blue",
            fg="white",
            command=show_email_page  # Excel sayfasına geçiş fonksiyonunu çağırır
        ).pack(pady=10)

        # Çıkış düğmesi
        tk.Button(
            self,
            text="Çıkış",
            font=("Arial", 14),
            bg="red",
            fg="white",
            command=master.destroy  # Uygulamayı kapatır
        ).pack(pady=10)
