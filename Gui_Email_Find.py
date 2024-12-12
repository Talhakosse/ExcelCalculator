import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import requests
from email_scraper import scrape_emails
from tkinter import ttk
import concurrent.futures
import re

class EmailPage(tk.Frame):
    def __init__(self, master, show_entry_page):
        print("Email page activated")
        super().__init__(master)

        # Sayfa başlığı
        tk.Label(self, text="Email Bul & Temizle", font=("Arial", 18, "bold")).pack(pady=20)

        # Bilgi etiketi
        tk.Label(self, text="Email tarama sayfası.", font=("Arial", 12)).pack(pady=10)

        # Dosya seçme düğmesi
        tk.Button(
            self,
            text="Email tarama",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.tara
        ).pack(pady=10)
        # Dosya seçme düğmesi
        tk.Button(
            self,
            text="Email temizleme",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.email_cleaner
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

 
    def tara(self):
        root = self.master  # EmailPage'in bağlı olduğu ana pencere

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
        
        def get_email_form_website(url):
            try:
                response = requests.get(url,timeout=5)
                if response.status_code == 200:
                    emails = scrape_emails(response.text)
                    return self.temizle(emails) # ilk olanı dönderir
                else:
                    print(f"Failed to access {url}: Status code {response.status_code}")
                    return None
            except Exception as e:
                print(f"Bir hata oluştu:   {e}")
                return None
            
        def process_excel_file(file_paths):
            print(f"Processing file: {file_paths}")

            for file in file_paths:
                DESTINATION_FOLDER = os.path.dirname(file)  # Excel dosyasının bulunduğu klasör
                print(DESTINATION_FOLDER)
                if file.endswith('.xlsx'):
                    df = pd.read_excel(file)  # Excel dosyasını oku
                    
                    if 'Website' not in df.columns:
                        print(f"'Website' column not found in {file}")
                        return

                elif file.endswith('.csv'):
                    df = pd.read_csv(file)  # CSV dosyasını oku

                    if 'Website' not in df.columns:
                        print(f"'Website' column not found in {file}")
                        return

                else:
                    messagebox.showwarning("Uyarı", f"Desteklenmeyen dosya formatı: {file}")
                    continue


                emails = []
                sayac = 1
                loading_window = tk.Toplevel(root)
                loading_window.title("Yükleniyor...")


                window_width = 200
                window_height = 75

                root.update_idletasks()  # Ana pencerenin güncel boyutlarını alabilmek için
                root_width = root.winfo_width()
                root_height = root.winfo_height()
                root_x = root.winfo_x()
                root_y = root.winfo_y()

                # Yüklenme penceresinin ana pencerenin ortasında olması için pozisyon hesaplama
                x_cordinate = root_x + (root_width//2) - (window_width//2)
                y_cordinate = root_y + (root_height//2) - (window_height//2)

                loading_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")


                
                # Sayaç göstergesi
                label = ttk.Label(loading_window, text=" 0 ")
                label.pack(pady=20)
                
                def fetch_email_and_update(website):
                    email = None
                    if pd.notna(website):
                        email = get_email_form_website(website)
                    return email


                websites = df['Website'].tolist()


                # Thread pool ile eş zamanlı olarak web sitelerini işle
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_website = {executor.submit(fetch_email_and_update, website): website for website in websites}
                    for future in concurrent.futures.as_completed(future_to_website):
                        email = future.result()
                        emails.append(email)
                        label.config(text=f" {sayac} / {len(websites)}")
                        loading_window.update()
                        sayac += 1
                        print(f"Email found: {email}")

                loading_window.destroy()  # Döngü bitince pencere kapanır

                df['Email'] = emails

        # Kaydetme işlemi
                if file.endswith('.xlsx'):
                    new_file_path = os.path.join(DESTINATION_FOLDER, f"Processed_{os.path.basename(file)}")
                    try:
                        df.to_excel(new_file_path, index=False)
                        messagebox.showinfo("Başarılı", "Dosyalar başarıyla birleştirildi ve kaydedildi!")

                        print(f"Processed file saved as: {new_file_path}")
                    except Exception as e:
                        print(f"Error saving {new_file_path}: {e}")

                elif file.endswith('.csv'):
                    new_file_path = os.path.join(DESTINATION_FOLDER, f"Processed_{os.path.basename(file)}")
                    try:
                        df.to_csv(new_file_path, index=False)
                        messagebox.showinfo("Başarılı", "Dosyalar başarıyla birleştirildi ve kaydedildi!")

                        print(f"Processed file saved as: {new_file_path}")
                    except Exception as e:
                        print(f"Error saving {new_file_path}: {e}")
        # Tek dosya işlemi
        process_excel_file(file_paths)


    def temizle(self, emails):
        domain_corrections = {
            'gmial.com': 'gmail.com',
            'gmaill.com': 'gmail.com',
            'yaho.com': 'yahoo.com',
            'outlok.com': 'outlook.com',
            'hotmial.com': 'hotmail.com',
            'coom': 'com',  # .coom hatalarını düzeltmek için
            # Daha fazla bilinen alan adlarını buraya ekleyebilirsiniz
        }


        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


        def clean_email(email):
            if not isinstance(email,str):
                return None

            # 1. E-posta adresindeki boşlukları ve gereksiz karakterleri temizleme
            email = email.strip().replace(' ', '').replace('%20', '')

            # 2. Eğer '//' gibi hatalı bir başlangıç varsa bunu kaldır
            email = re.sub(r'^//', '', email)

            # 3. Alan adı hatalarını düzelt
            for wrong_domain, correct_domain in domain_corrections.items():
                if wrong_domain in email:
                    email = email.replace(wrong_domain, correct_domain)

            return email

        def is_valid_email(email):
            # Geçerli bir e-posta adresi formatı olup olmadığını kontrol et
            if re.match(email_regex, email):
                return True
            return False

        def process_emails(email_list):
            cleaned_emails = []

            for email in email_list:
                cleaned_email = clean_email(email)
                # Eğer temizlenmiş e-posta adresi geçerli ise listeye ekle
                if cleaned_email and is_valid_email(cleaned_email):
                    cleaned_emails.append(cleaned_email)
                else:
                    cleaned_emails.append(None)  # Geçersiz e-posta için None ekle

            return cleaned_emails
        
        def get_email(emails):
            try:
                processed_emails = process_emails(emails)
                # Geçerli ve temizlenmiş ilk e-posta adresini döndür
                if processed_emails:
                    return processed_emails[0]
                else:
                    return None

            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        return  get_email(emails)

        
    def email_cleaner(self):
        root = self.master  # EmailPage'in bağlı olduğu ana pencere

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
            
        # Geçerli bir e-posta formatı kontrolü için kullanılacak regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Alan adı düzeltmeleri için bir eşleme tablosu
        domain_corrections = {
            'gmial.com': 'gmail.com',
            'gmaill.com': 'gmail.com',
            'yaho.com': 'yahoo.com',
            'outlok.com': 'outlook.com',
            'hotmial.com': 'hotmail.com',
            'coom': 'com',  # .coom hatalarını düzeltmek için
            # Daha fazla bilinen alan adlarını buraya ekleyebilirsiniz
        }

        def process_excel_file(file_paths):




            def clean_email(email):
                if not isinstance(email,str):
                    return None

                # 1. E-posta adresindeki boşlukları ve gereksiz karakterleri temizleme
                email = email.strip().replace(' ', '').replace('%20', '')

                # 2. Eğer '//' gibi hatalı bir başlangıç varsa bunu kaldır
                email = re.sub(r'^//', '', email)

                # 3. Alan adı hatalarını düzelt
                for wrong_domain, correct_domain in domain_corrections.items():
                    if wrong_domain in email:
                        email = email.replace(wrong_domain, correct_domain)

                return email

            def is_valid_email(email):
                # Geçerli bir e-posta adresi formatı olup olmadığını kontrol et
                if re.match(email_regex, email):
                    return True
                return False

            def process_emails(email_list):
                cleaned_emails = []

                for email in email_list:
                    cleaned_email = clean_email(email)
                    # Eğer temizlenmiş e-posta adresi geçerli ise listeye ekle
                    if cleaned_email and is_valid_email(cleaned_email):
                        cleaned_emails.append(cleaned_email)
                    else:
                        cleaned_emails.append(None)  # Geçersiz e-posta için None ekle

                return cleaned_emails



            for file in file_paths:
                DESTINATION_FOLDER = os.path.dirname(file)  # Excel dosyasının bulunduğu klasör

                print(f"Processing file: {file}")
                if file.endswith('.xlsx'):
                    try:
                        df = pd.read_excel(file)
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
                        return

                    if 'Email' not in df.columns:
                        print(f"'Email' column not found in {file}")
                        messagebox.showinfo("Başarısız", "Email kolonu bulunamadı!")

                        return
                elif file.endswith('.csv'):
                    try:
                        df= pd.read_csv(file)
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
                        return

                    if 'Email' not in df.columns:
                        messagebox.showinfo("Başarısız", "Email kolonu bulunamadı!")
                        print(f"'Email' column not found in {file}")
                        return
                    
                Emails = df['Email'].tolist()

                # E-posta sütununu temizleyelim ve geçersiz olanları silelim
                df['Cleaned Email'] = process_emails(Emails)

                # Geçerli olmayan (None olan) satırları temizlemek için dropna kullan
                df_cleaned = df.dropna(subset=['Cleaned Email'])

                # Temizlenmiş DataFrame'i kaydet
                cleaned_file_path = f"{DESTINATION_FOLDER}/cleaned_{file.split('/')[-1]}"
                if file.endswith('.xlsx'):
                    df_cleaned.to_excel(cleaned_file_path, index=False)
                    messagebox.showinfo("Başarılı", "Dosyalar başarıyla birleştirildi ve kaydedildi!")

                if file.endswith('.csv'):
                    df_cleaned.to_csv(cleaned_file_path, index=False)
                    messagebox.showinfo("Başarılı", "Dosyalar başarıyla birleştirildi ve kaydedildi!")

                print(f"Cleaned data saved to: {cleaned_file_path}")



        process_excel_file(file_paths)

