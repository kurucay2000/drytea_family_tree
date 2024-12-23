# Drytea Family Tree Builder

[![Unit Tests](https://github.com/IM-EB/sims_family_tree/actions/workflows/unit-tests-on-push.yml/badge.svg?branch=master)](https://github.com/IM-EB/sims_family_tree/actions/workflows/unit-tests-on-push.yml)

Aile ağaçları oluşturmak ve görselleştirmek için bir Python uygulaması - özellikle Sims'ler için! İlişkileri takip edin, aile üyeleri ekleyin ve tıpkı oyunda yaptığınız gibi karmaşık aile dinamiklerini görselleştirin.

## Özellikler

- Ayrıntılı bilgilerle aile üyelerini oluşturun ve yönetin
- İlişkileri takip edin (ebeveyn, eş, kardeş, vb.)
- Her Drytea özel ayrıntılar ekleyin (meslek, özellikler, yaşam aşaması, vb.)
- Etkileşimli grafiksel kullanıcı arayüzü
- Görsel aile ağacı temsili
- Aile ağaçlarını kaydet ve yükle
- Aile ağacı görselleştirmelerini resim olarak dışa aktarın

## Kurulum

### Ön Koşullar

- Python 3.8+
- uv (Python paket yöneticisi)

### Kurulum

1. Eğer henüz yüklemediyseniz uv'yi yükleyin:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Depoyu klonla:
```bash
git clone https://github.com/yourusername/sims-family-tree-builder.git
cd sims-family-tree-builder
```

3. Uygulamayı uv kullanarak çalıştırın:
```bash
uv run main.py
```

## Kullanımı

### Aile Ağacınızı Oluşturma

1. Yeni bir Drytea oluşturmak için "Üye Ekle"ye tıklayın
   - Adını, doğum tarihini ve cinsiyetini girin
   - Meslek, özellikler veya yaşam aşaması gibi özel bilgiler ekleyin

2. Drytea(s)inizin meta verilerini düzenleyin:
   - Aile soyunu takip etmek için babalarını/annelerini ekleyin
   - Yaşları, ölüm nedenleri veya önemli özellikleri gibi bilgileri ekleyin
   - Meta veriler her Drytea profilinde gösterilecek

3. Aile ağacını görüntüle:
   - Grafiksel bir sunum görmek için "Ağacı Görselleştir"e tıklayın
   - Mavi düğümler erkek Drytea'leri temsil ediyor
   - Pembe düğümler kadın Drytea'leri temsil ediyor
   - Kesintisiz çizgiler ebeveyn-çocuk ilişkilerini gösterir
   - Kesik çizgiler evlilikleri/ortaklıkları gösterir

## Proje Yapısı

TBD

## Bağımlılıklar

- tkinter - GUI framework
- networkx - Graph visualization
- matplotlib - Plotting and visualization
- matplotlib-backend-tkagg - GUI integration
