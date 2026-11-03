# lecture-notes-pipeline (Türkçe özet)

El yazısı ders notlarını **izlenebilir ve doğrulanmış** dijital ders kitaplarına dönüştüren, yapay
zekâ destekli bir üretim hattı. Ayrıntılı İngilizce açıklama: [README.md](README.md).

Yıldız Teknik Üniversitesi Matematik Mühendisliği'nde **bağımsız, gönüllü bir öğrenci projesidir**.
Resmî ya da hoca onaylı bir yayın değildir. Bu depo yalnız **sistemi** içerir: mimari, kurallar, ajan
brifleri, Typst şablonu ve doğrulama betikleri. Ders notu, taranmış sayfa, üretilmiş kitap ya da sınav
sorusu içermez. Örneklerin tamamı sentetiktir.

README'deki "girdi → çıktı" görselleri de sentetiktir: el yazısı görünümlü sayfa bu depo için üretilmiştir, gerçek bir hoca notu değildir.

## Temel fikirler

- **OCR kaynak değildir.** Her sayfa iki bağımsız ajan tarafından görüntüden okunur, farklar
  görüntüye bakılarak karara bağlanır.
- **Katmanlar ayrıdır.** Hocanın yazdığı ile yapay zekânın açıklaması, eklemesi ve çözümü etiketli
  ayrı katmanlarda durur. Hocanın hatası `[sic]` ile korunur, düzeltmesi ayrıca verilir.
- **Tahmin yoktur.** Okunamayan yer `[?]` ya da `Blocked` olarak işaretlenir.
- **Bağımsız denetim.** SymPy sonuçları sınar; her 10 kaynak sayfasına ayrı bir denetçi bakar ve
  yalnız rapor yazar; düzeltici her bulguyu uygulamadan önce yeniden sınar.
- **Son karar insanındır.** Hat kendi işine "tamamlandı" demez.

## Durum

- **Hazır 4 ders paketi:** Diferansiyel Denklemler, İstatistik, Lineer Programlama Teorisi, Mekanik.
- **Hazırlanıyor:** İleri Analiz.
- Paketler tam sürüm, telefon sürümü, sınav kitapçığı ve okuma rehberinden oluşur.
- Bölümün 300–400 kişilik sınıf gruplarında paylaşılıyor.
- **Sözel kol:** Hazır dizilmiş soru setlerinde kör çözücü, denetçi ve hakemle cevap doğrulama;
  bu depoda yalnızca sentetik örnekle gösterilir.

## Etik

Ders notları hocalarına aittir. Üretilen kitaplar yalnız sınıf içinde paylaşılır, burada
yayımlanmaz. Kitaplar özgün notun yerine geçmez; şüphede özgün sayfa esastır.
