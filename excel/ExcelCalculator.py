import tkinter as tk
from tkinter import filedialog, Label, PhotoImage, Button, messagebox, font
import pandas as pd
import os

def browse_folder1():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        project_excel_path_entry.delete(0, tk.END)
        project_excel_path_entry.insert(0, folder_selected)
        if folder_path_entry.get() != "Lütfen seçim yapiniz!":
            merge_button.config(state=tk.NORMAL, bg="yellow", foreground="midnight blue")

def browse_folder2():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_selected)
        if project_excel_path_entry.get() != "Lütfen seçim yapiniz!":
            merge_button.config(state=tk.NORMAL, bg="yellow", foreground="midnight blue")

def clear_button():
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, "Lütfen seçim yapiniz!")
    project_excel_path_entry.delete(0, tk.END)
    project_excel_path_entry.insert(0, "Lütfen seçim yapiniz!")
    text_box_f_name.insert(1.0," ")
    merge_button.config(state=tk.DISABLED)

def merge_excel_files(f_name):
    folder_path = project_excel_path_entry.get()
    target_path = folder_path_entry.get()
    if f_name == '':
        f_name = os.path.basename(folder_path)
    try:
        excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
        combined_df = pd.concat([pd.read_excel(os.path.join(folder_path, file)) for file in excel_files], ignore_index=True)
        save_combined_excel(combined_df, f_name, target_path)
        messagebox.showinfo("Başarılı", f"Dosyalar başarıyla birleştirildi ve '{os.path.basename(f_name)}.xlsx' olarak kaydedildi.")
        clear_button()
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def save_combined_excel(combined_df, f_name, target_path):
    full_path = os.path.join(target_path, f"{f_name}.xlsx")
    combined_df.to_excel(full_path, index=False)
    return full_path

def retrieve_input():
    input_text = text_box_f_name.get("1.0", tk.END)
    return input_text.strip()

def on_enter_key(event):
    merge_button.invoke()
    return "break"

# GUI oluşturma
root = tk.Tk()
root.title("Excel Birleştirici")
root.iconbitmap('table.ico')

root.geometry("600x350")
root.configure(bg='light grey')

floder_icon = PhotoImage(file='i1.png')

# Başlık etiketleri
folder_label = Label(root, text="Excel klasörünü seçin:", anchor="w", bg="light grey", font=("Arial", 10))
folder_label.place(x=10, y=20, width=120, height=30)
project_excel_path_entry = tk.Entry(root, width=50, font=("Arial", 10))
project_excel_path_entry.insert(0, "Lütfen seçim yapiniz!")
project_excel_path_entry.place(x=140, y=25, width=300)
browse_button = Button(root, image=floder_icon, command=browse_folder1, bg="white", borderwidth=0)
browse_button.place(x=450, y=18, width=30, height=30)

folder_label2 = Label(root, text="Kayıt Klasörünü seçin:", anchor="w", bg="light grey", font=("Arial", 10))
folder_label2.place(x=10, y=60, width=120, height=30)
folder_path_entry = tk.Entry(root, width=50, font=("Arial", 10))
folder_path_entry.insert(0, "Lütfen seçim yapiniz!")
folder_path_entry.place(x=140, y=65, width=300)
browse_button2 = Button(root, image=floder_icon, command=browse_folder2, bg="white", borderwidth=0)
browse_button2.place(x=450, y=58, width=30, height=30)

# Birleşik excel dosyasını isim verme kısmı
label1 = Label(root, text="Birleşik excel dosyasına isim verin:", bg="light grey", font=("Arial", 10))
label1.place(x=10, y=110, width=200)
text_box_f_name = tk.Text(root, height=1, width=30, font=("Arial", 10))
text_box_f_name.place(x=220, y=110, width=200)
text_box_f_name.bind("<Return>", on_enter_key)

label2 = Label(root, text="Eğer doldurmazsanız klasör ismi kullanılacak!", fg="red", bg="light grey", font=("Arial", 10, "bold"))
label2.place(x=150, y=140)

def combined_functions():
    f_name = retrieve_input()
    merge_excel_files(f_name)

merge_button = Button(root, text="Excel Dosyalarını Birleştir", bg="light yellow", fg="midnight blue", state=tk.DISABLED, command=combined_functions, font=("Arial", 10, "bold"))
merge_button.place(x=200, y=170, width=200)

root.mainloop()
