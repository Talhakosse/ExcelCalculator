import tkinter as tk
from Gui_Entry import EntryPage
from Gui_Excel import ExcelPage
from Gui_Email_Find import EmailPage

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Pencere ayarları
        self.title("Excel İşlemleri Uygulaması")
        self.geometry("600x300")
        self.iconbitmap("icon.ico")

        # Sayfaları saklamak için bir sözlük
        self.frames = {}

        # Sayfaları oluştur ve sakla
        self.frames["Entry"] = EntryPage(self, self.show_excel_page,self.show_email_page)
        self.frames["Excel"] = ExcelPage(self, self.show_entry_page)
        self.frames["Email_Find"] = EmailPage(self,self.show_entry_page)
        # Giriş sayfasını göster
        self.show_entry_page()

    def show_entry_page(self):
        # Entry sayfasını göster
        frame = self.frames["Entry"]
        frame.pack(fill="both", expand=True)

        # Diğer sayfayı gizle
        self.hide_other_pages(frame)


    def show_excel_page(self):
        # Excel sayfasını göster
        frame = self.frames["Excel"]
        frame.pack(fill="both", expand=True)

        # Diğer sayfayı gizle
        self.hide_other_pages(frame)


    def show_email_page(self):
        # EmailFind sayfasını göster
        frame = self.frames["Email_Find"]
        frame.pack(fill="both", expand=True)
        print("asda")

        # Diğer sayfayı gizle
        self.hide_other_pages(frame)

    def hide_other_pages(self, visible_frame):
        # Tüm sayfaları gizler, yalnızca belirtilen çerçeve görünür kalır
        for frame in self.frames.values():
            if frame is not visible_frame:
                frame.pack_forget()



# Uygulama başlatma
if __name__ == "__main__":
    app = Application()
    app.mainloop()
