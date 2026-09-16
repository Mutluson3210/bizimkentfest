# Araçlar

## basvuru_raporu.py — Başvuru Değerlendirme Raporu üreticisi

Google Form’dan indirilen Bizimkent FEST başvuru tablosunu (`.xlsx`) okuyup
başvuruları komisyon/kategori bazında sınıflandırır ve tıklanabilir
telefon (`tel:`), e-posta (`mailto:`) ve portfolyo/demo bağlantıları içeren
bir PDF rapor üretir.

### Kurulum

```bash
pip install openpyxl reportlab
```

### Kullanım

```bash
python3 araclar/basvuru_raporu.py "Bizimkent FEST Başvurular.xlsx" -o Rapor.pdf
```

### Raporun bölümleri

1. Festival Ekip Gönüllüleri
2. Gönüllü Sanatçılar (eser/portfolyo bağlantılarıyla)
3. Atölye / Workshop Komisyonu — gönüllü eğitmenler
4. Bizim Pazar — stand başvuruları (+ 4b: stand türü seçmiş ama başvuru
   kutusunu işaretlememiş, teyit edilmesi gereken kayıtlar)
5. Çocuk Atölyeleri ön kayıtları (çocuk adı, yaş, veli onayı)
6. Yetişkin Atölyeleri katılımcıları
7. Spor Komisyonu — Voleybol
8. Spor Komisyonu — Basketbol / Futbol
9. Bizim Star Ses Yarışması (demo ve referans bağlantılarıyla)
10. Sponsorluk
11. Kategori seçmemiş / takip edilecek başvurular
- EK-1: Mükerrer / eşleşen kayıt uyarıları
- EK-2: Tabloya sığmayan uzun açıklama metinleri

### KVKK notu

Başvuru tablosu ve üretilen PDF **kişisel veri içerir**; bu dosyalar bu depoya
eklenmez, yalnızca komisyon üyeleriyle paylaşılır.
