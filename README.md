# Excel Birleştirici Uygulaması

Bu uygulama, belirtilen iki klasör arasındaki Excel dosyalarını birleştiren ve yeni bir Excel dosyası olarak kaydeden basit bir Tkinter tabanlı araçtır. Uygulama, kullanıcı dostu bir arayüz sunarak işlemleri kolayca gerçekleştirmenizi sağlar.

## Özellikler

- Belirtilen klasördeki tüm Excel dosyalarını birleştirir.
- Birleşik dosyayı belirtilen hedef klasöre kaydeder.
- Kullanıcıya birleşik dosyanın adını belirleme seçeneği sunar.
- Eğer dosya adı belirtilmezse, kaynak klasör adı kullanılır.

## Gereksinimler

- Python 3.x
- Gerekli Python kütüphaneleri:
  - `tkinter`
  - `pandas`
  - `os`

## Kurulum

1. **Python 3.x** sürümünün sisteminizde yüklü olduğundan emin olun.
2. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install pandas
3.Proje dosyalarını bilgisayarınıza indirin ve bir dizine çıkarın.

## Kullanım
1. Uygulamayı başlatmak için merge_excel.py dosyasını çalıştırın:
python merge_excel.py
2. Uygulama arayüzü açıldığında, aşağıdaki adımları izleyin:
Excel Klasörünü Seçin: Birleştirmek istediğiniz Excel dosyalarının bulunduğu klasörü seçin.
Kayıt Klasörünü Seçin: Birleşik dosyayı kaydetmek istediğiniz klasörü seçin.
Birleşik Excel Dosyasına İsim Verin: İsteğe bağlı olarak birleşik dosya için bir ad girin. Eğer bu alanı boş bırakırsanız, kaynak klasör adı kullanılacaktır.
Excel Dosyalarını Birleştir butonuna tıklayın. Birleşme işlemi tamamlandığında, bir bilgi mesajı görüntülenecektir.
