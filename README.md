# 🐍 Modern Python Pip Paket Yöneticisi

Modern ve kullanıcı dostu bir grafik arayüzle Python paketlerinizi kolayca yönetin! Bu uygulama **ttkbootstrap** ile tasarlanmış modern dark tema ve Bootstrap stillerini kullanarak şık bir görünüm sunar.

## ✨ Özellikler

### 📦 Yüklü Paketler Yönetimi
- Tüm yüklü paketleri listeleyin ve boyutlarını görün
- Paketleri arayın ve filtreleyin
- Güncel olmayan paketleri tespit edin
- Paketleri tek tek veya toplu olarak güncelleyin
- Paketleri güvenle kaldırın
- Detaylı paket bilgilerini görüntüleyin

### 🔍 PyPI Paket Arama
- PyPI üzerinde paket arayın
- Paket detaylarını, açıklamalarını ve geliştiricilerini görün
- Paketleri doğrudan PyPI'dan yükleyin
- Gelişmiş kurulum seçenekleri (sürüm belirleme, --user, --upgrade vs.)

### 📄 Requirements.txt Yönetimi
- Requirements.txt dosyalarını açın ve düzenleyin
- Metin editörü ile paket listelerini özelleştirin
- Mevcut paketlerden requirements.txt oluşturun
- Requirements dosyasındaki tüm paketleri tek seferde yükleyin

### ⚙️ Sistem Ayarları ve Araçları
- Python ve pip sürüm bilgilerini görün
- Pip'i güncelleyin
- Pip önbelleğini temizleyin
- Bozuk paketleri tespit edin ve onarın
- Detaylı işlem logları

### 📊 Dışa Aktarma
- Paket listelerini farklı formatlarda dışa aktarın:
  - **TXT** (requirements.txt formatında)
  - **JSON** (metadata ile birlikte)
  - **CSV** (tablo formatında)

## 🚀 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- tkinter (genellikle Python ile birlikte gelir)

### 📥 Hazır EXE Dosyası İndirme
GitHub Releases sayfasından en son sürümü indirip doğrudan çalıştırabilirsiniz:
1. [Releases](https://github.com/hamer1818/pip-management/releases) sayfasına gidin
2. En son sürümü seçin
3. `ModernPipManager-Windows.zip` dosyasını indirin
4. Zip'i açın ve `ModernPipManager.exe` dosyasını çalıştırın

### Kurulum Adımları

1. **Projeyi klonlayın veya indirin:**
```bash
git clone <repository-url>
cd pip-management
```

2. **Gerekli bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```
veya manuel olarak:
```bash
pip install ttkbootstrap>=1.10.1
```

3. **Uygulamayı çalıştırın:**
```bash
python main.py
```

## 🎨 Ekran Görüntüleri ve Özellikler

### 📋 Yüklü Paketler Sekmesi
- **Renkli butonlar:** Her işlem için farklı Bootstrap renkleri
- **Arama özelliği:** Paketleri hızlıca filtreleyin
- **Sütun sıralama:** Paket adı, sürüm, boyut ve duruma göre sıralayın
- **Boyut hesaplama:** Her paketin disk kullanımını görün

### 🌐 Paket Arama Sekmesi
- **PyPI entegrasyonu:** Canlı paket arama
- **Detay paneli:** Seçili pakete ait açıklama ve bilgiler
- **Gelişmiş kurulum:** Özel sürüm ve parametre seçenekleri

### 📝 Requirements.txt Editörü
- **Söz dizimi vurgulama:** Koyu tema ile uyumlu
- **Horizontal/vertical scrollbar:** Büyük dosyalar için
- **Otomatik oluşturma:** Mevcut paketlerden requirements.txt

### 💻 Sistem Bilgileri
- **Python sürümü ve yolu**
- **Pip araçları** (güncelleme, önbellek temizleme)
- **Canlı log görüntüleme** koyu tema ile

## 🎯 Kullanım

### Paket Yükleme
1. **Paket Ara & Yükle** sekmesine gidin
2. Paket adını arama kutusuna yazın
3. **🔍 Ara** butonuna tıklayın
4. Listeden paketi seçin
5. **📦 Yükle** veya **⚙️ Gelişmiş Yükle** butonunu kullanın

### Paket Güncelleme
1. **📦 Yüklü Paketler** sekmesinde paketi seçin
2. **⬆️ Seçili Güncelle** butonuna tıklayın
3. Veya **🚀 Tümünü Güncelle** ile tüm paketleri güncelleyin

### Requirements.txt İşlemleri
1. **📄 Requirements.txt** sekmesine gidin
2. **📄 Dosya Aç** ile mevcut dosyayı yükleyin
3. Editörde düzenlemeler yapın
4. **💾 Dosya Kaydet** ile kaydedin
5. **📦 Tümünü Yükle** ile paketleri yükleyin

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **Python 3.7+**
- **ttkbootstrap** - Modern Bootstrap-inspired themes
- **tkinter** - GUI framework
- **subprocess** - Pip komut yürütme
- **threading** - Asenkron işlemler
- **json/urllib** - PyPI API entegrasyonu

### Proje Yapısı
```
pip-management/
├── main.py                 # Ana giriş noktası
├── pip_manager/
│   ├── __init__.py
│   ├── app.py             # Ana uygulama sınıfı
│   ├── ui.py              # UI bileşenleri
│   ├── handlers.py        # İş mantığı ve event handlers
│   └── utils.py           # Yardımcı fonksiyonlar
├── requirements.txt       # Proje bağımlılıkları
└── README.md             # Bu dosya
```

### Bootstrap Stil Temaları
Uygulama **darkly** temasını kullanır ve şu renk düzenini benimser:
- **info** (mavi) - Bilgilendirici işlemler
- **success** (yeşil) - Başarılı işlemler
- **warning** (turuncu) - Uyarı gerektiren işlemler
- **danger** (kırmızı) - Tehlikeli işlemler
- **primary** (mavi) - Birincil eylemler
- **secondary** (gri) - İkincil eylemler

## 🐛 Sorun Giderme

### Yaygın Hatalar

**"ModuleNotFoundError: No module named 'ttkbootstrap'"**
```bash
pip install ttkbootstrap
```

**"Permission denied" hataları**
- Windows'ta yönetici olarak çalıştırın
- Linux/Mac'te `sudo` kullanın veya virtual environment kullanın

**Pip komutları çalışmıyor**
- Python PATH ayarlarınızı kontrol edin
- `python -m pip` komutunu deneyin

### Log Dosyaları
Uygulama içindeki **⚙️ Ayarlar & Bilgi** sekmesinde tüm işlem loglarını görebilirsiniz.

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🤖 Otomatik Build ve Release

Bu proje GitHub Actions kullanarak otomatik build sistemi ile donatılmıştır:

### 🔄 Otomatik İşlemler
- **Her commit'te:** Otomatik exe dosyası oluşturulur
- **Otomatik versioning:** Tarih ve commit hash ile sürüm numarası oluşturulur
- **GitHub Releases:** Her build sonrası otomatik release oluşturulur
- **Zip paketi:** Exe dosyası otomatik olarak zip'lenir

### 📋 Build İşlemi
1. GitHub Actions, Windows Server'da Python 3.11 kurar
2. Bağımlılıkları yükler (`ttkbootstrap`, `pyinstaller`)
3. PyInstaller ile tek dosya halinde exe oluşturur
4. Exe'yi zip'ler ve GitHub Releases'e yükler

### 🏷️ Versioning Sistemi
```
v2024.01.15-1430-a1b2c3d
  │     │    │     │
  │     │    │     └── Commit hash (ilk 7 karakter)
  │     │    └────────── Saat (HHMM)
  │     └─────────────── Tarih (YYYY.MM.DD)
  └───────────────────── Version prefix
```

## 🙋‍♂️ Destek

Sorularınız veya önerileriniz için:
- Issue açın
- Pull request gönderin
- Dokümantasyonu kontrol edin
- GitHub Releases'den en son sürümü indirin

---

**Modern Python Pip Paket Yöneticisi** ile Python geliştirme deneyiminizi geliştirin! 🚀 